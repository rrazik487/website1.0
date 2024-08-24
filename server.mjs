import express from 'express';
import dotenv from 'dotenv';
import fetch from 'node-fetch'; // Use import for ES Modules
import bodyParser from 'body-parser';
import mysql from 'mysql';
import path from 'path';
import { fileURLToPath } from 'url';


// Load environment variables from .env file
dotenv.config();

// Get the directory name of the current module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize Express app
const app = express();
const port = 3001;

// MySQL connection setup
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'r', // replace with your MySQL root password
    database: 'symptoms_checker'
});

// Connect to MySQL
db.connect(err => {
    if (err) {
        console.error('Database connection error:', err);
        return;
    }
    console.log('Connected to MySQL database');
});
// Middleware
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Define a basic route for the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'symptoms-checker-chatbot','public'));
});

// Load Gemini API key from environment variables
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

// Endpoint for checking symptoms
app.post('/api/check-symptoms', async (req, res) => {
    const { symptoms } = req.body;

    // Define request options for the Gemini API
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${GEMINI_API_KEY}`
        },
        body: JSON.stringify({ symptoms })
    };

    try {
        // Make a request to the Gemini API
        const response = await fetch('https://api.gemini.com/v1/symptoms', options);
        const data = await response.json();
        // Return the API response back to the client
        res.json({ response: data.message });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.post('/api/add-prescription', (req, res) => {
    const { user_id, symptoms, diagnosis } = req.body;

    const query = 'INSERT INTO prescriptions (user_id, symptoms, diagnosis) VALUES (?, ?, ?)';
    db.query(query, [user_id, symptoms, diagnosis], (err, result) => {
        if (err) {
            console.error('Database error:', err);
            res.status(500).json({ error: 'Database error' });
            return;
        }
        res.json({ message: 'Prescription added successfully' });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
