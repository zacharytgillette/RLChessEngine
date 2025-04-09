import ftplib
import hashlib
import json
import os
from logging import getLogger

import tensorflow as tf
from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers import Lambda, Reshape, Permute, Multiply, GlobalAveragePooling2D
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation, Dense, Flatten
from keras.layers.merge import Add, Concatenate
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2

from chess_zero.agent.api_chess import ChessModelAPI
from chess_zero.config import Config
logger = getLogger(__name__)
class EnhancedChessModel:
    """
    Enhanced chess model with attention mechanisms and advanced architectural patterns.

    Attributes:
        :ivar Config config: configuration to use
        :ivar Model model: the Keras model to use for predictions
        :ivar digest: hash of the weights file
        :ivar ChessModelAPI api: API for model prediction
    """

    def __init__(self, config: Config):
        self.config = config
        self.model = None  # type: Model
        self.digest = None
        self.api = None

    def get_pipes(self, num=1):
        """
        Creates pipes for receiving observations and returning predictions.

        :param int num: number of pipes to create
        :return: list of connections to created pipes
        """
        if self.api is None:
            self.api = ChessModelAPI(self)
            self.api.start()
        return [self.api.create_pipe() for _ in range(num)]

    def build(self):
        """
        Builds the enhanced Keras model with attention mechanism and improved blocks.
        """
        mc = self.config.model
        in_x = x = Input((18, 8, 8))  # Chess input: 18 planes of 8x8 board

        # Initial convolution block
        x = Conv2D(filters=mc.cnn_filter_num, kernel_size=mc.cnn_first_filter_size, padding="same",
                   data_format="channels_first", use_bias=False, kernel_regularizer=l2(mc.l2_reg),
                   name="input_conv-" + str(mc.cnn_first_filter_size) + "-" + str(mc.cnn_filter_num))(x)
        x = BatchNormalization(axis=1, name="input_batchnorm")(x)
        x = Activation("relu", name="input_relu")(x)

        # Build enhanced residual tower with attention
        skip_connections = []
        for i in range(mc.res_layer_num):
            x = self._build_enhanced_residual_block(x, i + 1)

            # Store skip connections for dense network pattern
            if i % 2 == 0 and i > 0:  # Every other layer after the first
                skip_connections.append(x)

        # Add self-attention mechanism after residual blocks
        attention_out = self._build_self_attention(x)

        # Add dense connections if we have skip connections
        if skip_connections:
            for skip in skip_connections:
                # Match dimensions if needed with 1x1 conv
                if skip.shape[1] != attention_out.shape[1]:
                    skip = Conv2D(filters=attention_out.shape[1], kernel_size=1,
                                  data_format="channels_first", use_bias=False,
                                  kernel_regularizer=l2(mc.l2_reg))(skip)
                attention_out = Add()([attention_out, skip])

        # Enhanced policy head
        policy_head = self._build_enhanced_policy_head(attention_out)

        # Enhanced value head
        value_head = self._build_enhanced_value_head(attention_out)

        self.model = Model(in_x, [policy_head, value_head], name="enhanced_chess_model")

    def _build_enhanced_residual_block(self, x, index):
        """
        Builds an enhanced residual block with squeeze-and-excitation.

        :param x: input tensor
        :param index: block index
        :return: output tensor
        """
        mc = self.config.model
        in_x = x
        res_name = f"res{index}"

        # First convolution
        x = Conv2D(filters=mc.cnn_filter_num, kernel_size=mc.cnn_filter_size, padding="same",
                   data_format="channels_first", use_bias=False, kernel_regularizer=l2(mc.l2_reg),
                   name=f"{res_name}_conv1-{mc.cnn_filter_size}-{mc.cnn_filter_num}")(x)
        x = BatchNormalization(axis=1, name=f"{res_name}_batchnorm1")(x)
        x = Activation("relu", name=f"{res_name}_relu1")(x)

        # Second convolution
        x = Conv2D(filters=mc.cnn_filter_num, kernel_size=mc.cnn_filter_size, padding="same",
                   data_format="channels_first", use_bias=False, kernel_regularizer=l2(mc.l2_reg),
                   name=f"{res_name}_conv2-{mc.cnn_filter_size}-{mc.cnn_filter_num}")(x)
        x = BatchNormalization(axis=1, name=f"{res_name}_batchnorm2")(x)

        # Squeeze-and-Excitation block (channel attention)
        se = GlobalAveragePooling2D(data_format="channels_first", name=f"{res_name}_se_gap")(x)
        se = Reshape((mc.cnn_filter_num, 1, 1), name=f"{res_name}_se_reshape")(se)
        se = Conv2D(filters=mc.cnn_filter_num // 16, kernel_size=1, use_bias=True,
                    data_format="channels_first", name=f"{res_name}_se_reduce")(se)
        se = Activation("relu", name=f"{res_name}_se_relu")(se)
        se = Conv2D(filters=mc.cnn_filter_num, kernel_size=1, use_bias=True,
                    data_format="channels_first", name=f"{res_name}_se_expand")(se)
        se = Activation("sigmoid", name=f"{res_name}_se_sigmoid")(se)

        # Apply channel attention
        x = Multiply(name=f"{res_name}_se_excite")([x, se])

        # Skip connection
        x = Add(name=f"{res_name}_add")([in_x, x])
        x = Activation("relu", name=f"{res_name}_relu2")(x)

        return x

    def _build_self_attention(self, x):
        """
        Builds a spatial self-attention mechanism to capture piece relationships.

        :param x: input tensor
        :return: attention-enhanced tensor
        """
        mc = self.config.model

        # Generate query, key, value projections
        query = Conv2D(filters=mc.cnn_filter_num // 2, kernel_size=1,
                       data_format="channels_first", use_bias=True,
                       name="attn_query")(x)
        key = Conv2D(filters=mc.cnn_filter_num // 2, kernel_size=1,
                     data_format="channels_first", use_bias=True,
                     name="attn_key")(x)
        value = Conv2D(filters=mc.cnn_filter_num, kernel_size=1,
                       data_format="channels_first", use_bias=True,
                       name="attn_value")(x)

        # Reshape for attention calculation
        batch_size = tf.shape(x)[0]
        query = Reshape((mc.cnn_filter_num // 2, 64))(query)  # 64 = 8x8 board
        key = Reshape((mc.cnn_filter_num // 2, 64))(key)
        value = Reshape((mc.cnn_filter_num, 64))(value)

        # Transpose for matrix multiplication
        query = Permute((2, 1))(query)  # (batch, 64, channels//2)
        key = Permute((1, 2))(key)  # (batch, channels//2, 64)
        value = Permute((2, 1))(value)  # (batch, 64, channels)

        # Calculate attention scores
        attention_scores = Lambda(lambda inputs: tf.matmul(inputs[0], inputs[1]) /
                                                 tf.sqrt(tf.cast(mc.cnn_filter_num // 2, tf.float32)),
                                  name="attn_scores")([query, key])
        attention_weights = Activation("softmax", name="attn_weights")(attention_scores)

        # Apply attention weights to value
        context = Lambda(lambda inputs: tf.matmul(inputs[0], inputs[1]),
                         name="attn_context")([attention_weights, value])

        # Reshape back to spatial representation
        context = Reshape((mc.cnn_filter_num, 8, 8))(context)

        # Residual connection
        return Add(name="attn_residual")([x, context])

    def _build_enhanced_policy_head(self, x):
        """
        Builds an enhanced policy head with chess-specific considerations.

        :param x: input tensor
        :return: policy output tensor
        """
        mc = self.config.model

        # Policy head with multiple pathways
        p1 = Conv2D(filters=32, kernel_size=3, padding="same", data_format="channels_first",
                    use_bias=False, kernel_regularizer=l2(mc.l2_reg), name="policy_conv1")(x)
        p1 = BatchNormalization(axis=1, name="policy_bn1")(p1)
        p1 = Activation("relu", name="policy_relu1")(p1)

        p2 = Conv2D(filters=32, kernel_size=1, data_format="channels_first",
                    use_bias=False, kernel_regularizer=l2(mc.l2_reg), name="policy_conv2")(x)
        p2 = BatchNormalization(axis=1, name="policy_bn2")(p2)
        p2 = Activation("relu", name="policy_relu2")(p2)

        # Combine policy pathways
        p = Concatenate(axis=1, name="policy_concat")([p1, p2])

        # Final policy convolution
        p = Conv2D(filters=2, kernel_size=1, data_format="channels_first",
                   use_bias=False, kernel_regularizer=l2(mc.l2_reg), name="policy_conv_final")(p)
        p = BatchNormalization(axis=1, name="policy_bn_final")(p)
        p = Activation("relu", name="policy_relu_final")(p)

        # Flatten and produce final policy output
        p = Flatten(name="policy_flatten")(p)
        policy_out = Dense(self.config.n_labels, kernel_regularizer=l2(mc.l2_reg),
                           activation="softmax", name="policy_out")(p)

        return policy_out

    def _build_enhanced_value_head(self, x):
        """
        Builds an enhanced value head for better position evaluation.

        :param x: input tensor
        :return: value output tensor
        """
        mc = self.config.model

        # Value convolution pathway
        v = Conv2D(filters=8, kernel_size=1, data_format="channels_first",
                   use_bias=False, kernel_regularizer=l2(mc.l2_reg), name="value_conv")(x)
        v = BatchNormalization(axis=1, name="value_bn")(v)
        v = Activation("relu", name="value_relu")(v)

        # Global spatial features
        v = Flatten(name="value_flatten")(v)

        # Two hidden layers for value approximation
        v = Dense(mc.value_fc_size, kernel_regularizer=l2(mc.l2_reg),
                  activation="relu", name="value_dense1")(v)
        v = Dense(mc.value_fc_size // 2, kernel_regularizer=l2(mc.l2_reg),
                  activation="relu", name="value_dense2")(v)

        # Final value output
        value_out = Dense(1, kernel_regularizer=l2(mc.l2_reg),
                          activation="tanh", name="value_out")(v)

        return value_out

    @staticmethod
    def fetch_digest(weight_path):
        """
        Calculates the SHA-256 digest of the weights file.

        :param weight_path: path to the weights file
        :return: hex digest string
        """
        if os.path.exists(weight_path):
            m = hashlib.sha256()
            with open(weight_path, "rb") as f:
                m.update(f.read())
            return m.hexdigest()

    def load(self, config_path, weight_path):
        """
        Loads the model configuration and weights.

        :param config_path: path to the configuration file
        :param weight_path: path to the weights file
        :return: True if loading was successful
        """
        mc = self.config.model
        resources = self.config.resource

        # Try loading from distributed server if configured
        if mc.distributed and config_path == resources.model_best_config_path:
            try:
                logger.debug("loading model from server")
                ftp_connection = ftplib.FTP(resources.model_best_distributed_ftp_server,
                                            resources.model_best_distributed_ftp_user,
                                            resources.model_best_distributed_ftp_password)
                ftp_connection.cwd(resources.model_best_distributed_ftp_remote_path)
                ftp_connection.retrbinary("RETR model_best_config.json", open(config_path, 'wb').write)
                ftp_connection.retrbinary("RETR model_best_weight.h5", open(weight_path, 'wb').write)
                ftp_connection.quit()
            except:
                logger.warning("Could not load model from server")

        # Load from local files
        if os.path.exists(config_path) and os.path.exists(weight_path):
            logger.debug(f"loading model from {config_path}")
            with open(config_path, "rt") as f:
                self.model = Model.from_config(json.load(f))
            self.model.load_weights(weight_path)
            self.model._make_predict_function()
            self.digest = self.fetch_digest(weight_path)
            logger.debug(f"loaded model digest = {self.digest}")
            return True
        else:
            logger.debug(f"model files do not exist at {config_path} and {weight_path}")
            return False

    def save(self, config_path, weight_path):
        """
        Saves the model configuration and weights.

        :param config_path: path to save the configuration
        :param weight_path: path to save the weights
        """
        logger.debug(f"save model to {config_path}")
        with open(config_path, "wt") as f:
            json.dump(self.model.get_config(), f)
            self.model.save_weights(weight_path)
        self.digest = self.fetch_digest(weight_path)
        logger.debug(f"saved model digest {self.digest}")

        # Upload to distributed server if configured
        mc = self.config.model
        resources = self.config.resource
        if mc.distributed and config_path == resources.model_best_config_path:
            try:
                logger.debug("saving model to server")
                ftp_connection = ftplib.FTP(resources.model_best_distributed_ftp_server,
                                            resources.model_best_distributed_ftp_user,
                                            resources.model_best_distributed_ftp_password)
                ftp_connection.cwd(resources.model_best_distributed_ftp_remote_path)

                with open(config_path, 'rb') as fh:
                    ftp_connection.storbinary('STOR model_best_config.json', fh)

                with open(weight_path, 'rb') as fh:
                    ftp_connection.storbinary('STOR model_best_weight.h5', fh)

                ftp_connection.quit()
                logger.debug("model successfully uploaded to server")
            except Exception as e:
                logger.warning(f"Failed to upload model to server: {str(e)}")