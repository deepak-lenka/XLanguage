import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Select,
  MenuItem,
  CircularProgress,
} from '@mui/material';
import axios from 'axios';

const API_URL = 'https://xlanguage.iamdeepak034.workers.dev/api';

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [targetLanguage, setTargetLanguage] = useState('English');
  const [loading, setLoading] = useState(false);

  const languages = [
    'English', 'Spanish', 'French', 'German', 'Chinese', 
    'Japanese', 'Korean', 'Arabic', 'Hindi', 'Swahili'
  ];

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message,
        target_language: targetLanguage,
      });

      setMessages([
        ...messages,
        { text: message, type: 'user' },
        { text: response.data.response, type: 'bot' },
      ]);
      setMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          XLanguage Chat
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Select
            value={targetLanguage}
            onChange={(e) => setTargetLanguage(e.target.value)}
            fullWidth
          >
            {languages.map((lang) => (
              <MenuItem key={lang} value={lang}>
                {lang}
              </MenuItem>
            ))}
          </Select>
        </Box>

        <Box sx={{ height: '400px', overflowY: 'auto', mb: 2, p: 2 }}>
          {messages.map((msg, index) => (
            <Box
              key={index}
              sx={{
                mb: 1,
                textAlign: msg.type === 'user' ? 'right' : 'left',
              }}
            >
              <Paper
                sx={{
                  display: 'inline-block',
                  p: 1,
                  px: 2,
                  backgroundColor: msg.type === 'user' ? '#e3f2fd' : '#f5f5f5',
                  maxWidth: '70%',
                }}
              >
                <Typography>{msg.text}</Typography>
              </Paper>
            </Box>
          ))}
        </Box>

        <form onSubmit={sendMessage}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message..."
              disabled={loading}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Send'}
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
}

export default App;
