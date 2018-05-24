const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors({origin: 'http://localhost:8080'}));

app.post('/tmd', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  setTimeout(() => {
    res.send('{"morph_service/classifier/training_sample/L5_TPC_A": 0.1, "morph_service/classifier/training_sample/L5_UPC": 0.1, "morph_service/classifier/training_sample/L5_TPC_C": 0.0, "morph_service/classifier/training_sample/L5_TPC_B": 0.8}');
  }, 2000);
});

app.listen(3000, () => console.log('Example app listening on port 3000!'));
