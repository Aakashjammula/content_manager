import torch
import torch.nn as nn
import torch.nn.functional as F

LSTM_UNITS = 128
DENSE_HIDDEN_UNITS = 4 * LSTM_UNITS

class NeuralNet(nn.Module):
    
    def __init__(self, embedding_matrix, num_aux_targets, max_features):
        super(NeuralNet, self).__init__()

        embed_size = embedding_matrix.shape[1]

        self.embedding = nn.Embedding(max_features, embed_size)
        self.embedding.weight = nn.Parameter(torch.tensor(embedding_matrix, dtype=torch.float32))
        self.embedding.weight.requires_grad = False

        self.embedding_dropout = nn.Dropout(0.3)

        self.lstm1 = nn.LSTM(
            embed_size,
            LSTM_UNITS,
            bidirectional=True,
            batch_first=True
        )

        self.lstm2 = nn.LSTM(
            LSTM_UNITS * 2,
            LSTM_UNITS,
            bidirectional=True,
            batch_first=True
        )

        self.linear1 = nn.Linear(DENSE_HIDDEN_UNITS, DENSE_HIDDEN_UNITS)
        self.linear2 = nn.Linear(DENSE_HIDDEN_UNITS, DENSE_HIDDEN_UNITS)
        self.linear_out = nn.Linear(DENSE_HIDDEN_UNITS, 1)
        self.linear_aux_out = nn.Linear(DENSE_HIDDEN_UNITS, num_aux_targets)

    def forward(self, x):
        h_embedding = self.embedding(x)
        h_embedding = self.embedding_dropout(h_embedding)

        h_lstm1, _ = self.lstm1(h_embedding)
        h_lstm2, _ = self.lstm2(h_lstm1)

        # Global average pooling
        avg_pool = torch.mean(h_lstm2, 1)

        # Global max pooling
        max_pool, _ = torch.max(h_lstm2, 1)

        h_conc = torch.cat((max_pool, avg_pool), 1)

        h_conc_linear1 = F.relu(self.linear1(h_conc))
        h_conc_linear2 = F.relu(self.linear2(h_conc))

        hidden = h_conc + h_conc_linear1 + h_conc_linear2

        result = self.linear_out(hidden)
        aux_result = self.linear_aux_out(hidden)
        out = torch.cat([result, aux_result], 1)

        return out

    def save_model(self, file_path):
        torch.save({
            'model_state_dict': self.state_dict()
        }, file_path)