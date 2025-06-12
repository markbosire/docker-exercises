const express = require('express');
const { Pool } = require('pg');

const app = express();

// Connect to database using container name!
const pool = new Pool({
  host: 'database',  // ← This is the magic!
  user: 'postgres',
  password: 'secret',
  database: 'postgres'
});

app.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({ 
      message: 'Connected to database using name "database"!',
      time: result.rows[0].now 
    });
  } catch (err) {
    res.json({ error: err.message });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
