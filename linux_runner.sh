#!/bin/bash

echo "========================================="
echo "       Sudoku CSP Solver Test Suite      "
echo "========================================="
echo ""

echo "Testing Easy Board..."
python3 main.py data/easy.txt
echo ""
echo "-----------------------------------------"
echo ""

echo "Testing Medium Board..."
python3 main.py data/medium.txt
echo ""
echo "-----------------------------------------"
echo ""

echo "Testing Hard Board..."
python3 main.py data/hard.txt
echo ""
echo "-----------------------------------------"
echo ""

echo "Testing Expert Board..."
python3 main.py data/expert.txt
echo ""
echo "========================================="
echo "All tests complete!"
