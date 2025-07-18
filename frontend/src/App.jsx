import React, { useState, useEffect } from "react";
import {
  Container, Typography, Slider, Grid, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Box, TextField, Button
} from "@mui/material";

const defaultWeights = {
  w1: 0.35, w2: 0.25, w3: 0.25, w4: 0.10, w5: 0.05,
  a1: 0.8, a2: 0.1, b1: 0.1, b2: 0.3, decay_constant: 0.1,
  inflection: 120.0, steepness: 20.0
};

const weightLabels = {
  w1: "w₁ (Shares/Reposts)", w2: "w₂ (Other Interactions)", w3: "w₃ (Comments/Replies)",
  w4: "w₄ (Likes/Dislikes)", w5: "w₅ (Views)",
  a1: "a₁ (Like Weight)", a2: "a₂ (Dislike Weight)",
  b1: "b₁ (Cursory View Weight)", b2: "b₂ (Engaged View Weight)",
  decay_constant: "Decay Constant",
  inflection: "Inflection Point (Logistic)",
  steepness: "Steepness (Logistic)"
};

function App() {
  const [weights, setWeights] = useState(defaultWeights);
  const [data, setData] = useState([]);
  const [columns, setColumns] = useState([]);

  // Fetch scores from backend
  const fetchScores = async (params) => {
    const res = await fetch("http://localhost:8000/scores", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params)
    });
    const json = await res.json();
    setColumns(json.columns);
    setData(json.data);
  };

  useEffect(() => {
    fetchScores(weights);
    // eslint-disable-next-line
  }, []);

  // Update scores when weights change
  const handleWeightChange = (key, value) => {
    const newWeights = { ...weights, [key]: value };
    setWeights(newWeights);
    fetchScores(newWeights);
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        ThreadScorer Demo
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Adjust the weights and decay constant below. Scores update instantly!
      </Typography>
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2}>
          {Object.keys(defaultWeights).map((key) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={key}>
              <Typography gutterBottom>{weightLabels[key]}</Typography>
              {key === "decay_constant" ? (
                <TextField
                  type="number"
                  value={weights[key]}
                  inputProps={{ step: 0.01, min: 0.01, max: 1 }}
                  onChange={e => handleWeightChange(key, parseFloat(e.target.value))}
                  fullWidth
                  size="small"
                />
              ) : (
                <Slider
                  value={weights[key]}
                  min={0}
                  max={key.startsWith("w") ? 1 : 2}
                  step={0.01}
                  onChange={(_, v) => handleWeightChange(key, v)}
                  valueLabelDisplay="auto"
                />
              )}
            </Grid>
          ))}
        </Grid>
      </Box>
      <Button
        variant="contained"
        color="secondary"
        onClick={() => {
          setWeights(defaultWeights);
          fetchScores(defaultWeights);
        }}
        sx={{ mb: 2 }}
      >
        Reset to Default
      </Button>
      <Typography variant="h6" gutterBottom>
        Thread Scores
      </Typography>
      <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
        <Table stickyHeader size="small">
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={col}>{col.replace(/_/g, " ")}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, idx) => (
              <TableRow key={row.thread_id || idx}>
                {columns.map((col) => (
                  <TableCell key={col}>
                    {typeof row[col] === "number"
                      ? row[col].toFixed(2)
                      : row[col]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
}

export default App;