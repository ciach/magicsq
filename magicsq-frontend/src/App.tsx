import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import magicSquaresData from './pl_magic_squares.json';
import magicSquaresPrompts from './pl_magic_squares_pytania.json';

interface MagicSquare {
  [key: string]: string;
}

interface MagicSquaresData {
  [key: string]: MagicSquare;
}

interface MagicSquaresPrompts {
  [key: string]: MagicSquare;
}

function App() {
  const [currentSquareId, setCurrentSquareId] = useState<string>("1");
  const [board, setBoard] = useState<string[][]>(Array(5).fill(null).map(() => Array(5).fill("")));
  const [hoveredRow, setHoveredRow] = useState<number | null>(null);
  const [hoveredCol, setHoveredCol] = useState<number | null>(null);
  const [selectedRow, setSelectedRow] = useState<number | null>(null);
  const [inputWord, setInputWord] = useState<string>("");
  const [incorrectWords, setIncorrectWords] = useState<string[]>([]);
  const [completedRows, setCompletedRows] = useState<number[]>([]);
  const [completedCols, setCompletedCols] = useState<number[]>([]);
  
  // Create refs for the board and input elements
  const boardRef = useRef<HTMLDivElement>(null);
  const inputBoxRef = useRef<HTMLDivElement>(null);

  // Type assertions to ensure TypeScript recognizes our data structure
  const squares = magicSquaresData as MagicSquaresData;
  const prompts = magicSquaresPrompts as MagicSquaresPrompts;

  // Get the current magic square
  const currentSquare = squares[currentSquareId];
  const currentPrompts = prompts[currentSquareId];

  // Handle row hover
  const handleRowHover = (rowIndex: number | null) => {
    setHoveredRow(rowIndex);
    setHoveredCol(rowIndex); // In a magic square, we highlight the same column as the row
  };

  // Handle row click
  const handleRowClick = (rowIndex: number) => {
    if (completedRows.includes(rowIndex)) {
      return; // Don't allow editing completed rows
    }
    
    setSelectedRow(rowIndex);
    setInputWord("");
  };

  // Handle document click to dismiss input field when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      // If input is open and click is outside the board and input box
      if (
        selectedRow !== null && 
        boardRef.current && 
        inputBoxRef.current && 
        !boardRef.current.contains(event.target as Node) && 
        !inputBoxRef.current.contains(event.target as Node)
      ) {
        setSelectedRow(null);
        setInputWord("");
      }
    };

    // Add event listener
    document.addEventListener('mousedown', handleClickOutside);
    
    // Clean up the event listener
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [selectedRow]);

  // Handle word submission
  const handleSubmitWord = () => {
    if (selectedRow === null) return;
    
    const correctWord = currentSquare[selectedRow.toString()];
    
    if (inputWord.toLowerCase() === correctWord.toLowerCase()) {
      // Word is correct
      const newBoard = [...board];
      
      // Fill in the row
      for (let i = 0; i < 5; i++) {
        newBoard[selectedRow][i] = correctWord[i];
      }
      
      // Fill in the column (same word appears in the column in a magic square)
      for (let i = 0; i < 5; i++) {
        newBoard[i][selectedRow] = correctWord[i];
      }
      
      setBoard(newBoard);
      setCompletedRows([...completedRows, selectedRow]);
      setCompletedCols([...completedCols, selectedRow]);
    } else {
      // Word is incorrect
      setIncorrectWords([...incorrectWords, inputWord]);
    }
    
    setSelectedRow(null);
    setInputWord("");
  };

  // Handle square selection
  const handleSquareChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setCurrentSquareId(e.target.value);
    setBoard(Array(5).fill(null).map(() => Array(5).fill("")));
    setCompletedRows([]);
    setCompletedCols([]);
    setIncorrectWords([]);
    setSelectedRow(null);
  };

  // Handle key press for word input
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmitWord();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Magic Word Squares</h1>
        <div className="square-selector">
          <label htmlFor="square-select">Choose a magic square: </label>
          <select 
            id="square-select" 
            value={currentSquareId} 
            onChange={handleSquareChange}
          >
            {Object.keys(squares).map(id => (
              <option key={id} value={id}>Magic Square {id}</option>
            ))}
          </select>
        </div>
      </header>
      
      <main>
        <div className="game-container">
          {/* Hint box above the board - always present but only shows content when hovering or selected */}
          <div className="prompt-box">
            {hoveredRow !== null ? (
              <p>{currentPrompts[hoveredRow.toString()]}</p>
            ) : selectedRow !== null ? (
              <p>{currentPrompts[selectedRow.toString()]}</p>
            ) : (
              <p className="placeholder-text">Hover over a row to see the hint</p>
            )}
          </div>
          
          <div className="board" ref={boardRef}>
            {board.map((row, rowIndex) => (
              <div 
                key={rowIndex} 
                className={`board-row ${hoveredRow === rowIndex ? 'hovered' : ''} ${completedRows.includes(rowIndex) ? 'completed' : ''} ${selectedRow === rowIndex ? 'selected' : ''}`}
                onMouseEnter={() => handleRowHover(rowIndex)}
                onMouseLeave={() => handleRowHover(null)}
                onClick={() => handleRowClick(rowIndex)}
              >
                {row.map((cell, cellIndex) => (
                  <div 
                    key={cellIndex} 
                    className={`board-cell ${completedCols.includes(cellIndex) ? 'completed-col' : ''} ${hoveredCol === cellIndex ? 'hovered-col' : ''}`}
                  >
                    {cell}
                  </div>
                ))}
              </div>
            ))}
          </div>
          
          {/* Input box below the board */}
          {selectedRow !== null && (
            <div className="input-box" ref={inputBoxRef}>
              <input 
                type="text" 
                value={inputWord} 
                onChange={(e) => setInputWord(e.target.value)} 
                onKeyPress={handleKeyPress}
                maxLength={5}
                autoFocus
                placeholder="Type your answer..."
              />
              <button onClick={handleSubmitWord}>Submit</button>
            </div>
          )}
          
          {incorrectWords.length > 0 && (
            <div className="incorrect-words">
              <h3>Incorrect Attempts:</h3>
              <ul>
                {incorrectWords.map((word, index) => (
                  <li key={index} className="strikethrough">{word}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
