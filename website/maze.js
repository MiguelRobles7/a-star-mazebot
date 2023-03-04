class Maze {
  _canvas;
  _cellSize;
  _size; //readOnly
  cells = [];
  _PADDING = 10;

  constructor(canvas, size) {
    this._canvas = canvas.getContext("2d");
    this._canvas.clearRect(0, 0, canvas.width, canvas.height);
    this._cellSize = (canvas.width - this._PADDING * 2) / size;
    this._size = size;
    for (let i = 0; i < size; i++) {
      const row = [];
      for (let j = 0; j < size; j++) row.push(new Cell(this, i, j));
      this.cells.push(row);
    }
  }

  get size() {
    return this._size;
  }

  cell(x, y) {
    return this.cells[x][y];
  }
  _cellPos(x, y) {
    return {
      x: this._PADDING + x * this._cellSize,
      y: this._PADDING + y * this._cellSize,
    };
  }
  cellColor(x, y, color) {
    const c = this._canvas;
    const size = this._cellSize;
    const pos = this._cellPos(x, y);

    c.fillStyle = color;
    c.fillRect(pos.x, pos.y, size, size);
    c.strokeStyle = "black";
    c.strokeRect(pos.x, pos.y, size, size);
  }
  cellText(x, y, text) {
    //TODO
  }
}
class Cell {
  _maze;
  _x;
  _y;
  _color;
  _text;
  value;

  constructor(maze, x, y, color, text) {
    this._maze = maze;
    this._x = x;
    this._y = y;
    if (color) this.color = color;
    if (text) this.text = text;
  }

  get x() {
    return this._x;
  }
  get y() {
    return this._y;
  }

  get color() {
    return this._color;
  }
  set color(color) {
    this._maze.cellColor(this._x, this._y, color);
    this._color = color;
  }

  get text() {
    return this._text;
  }
  set text(text) {
    this._maze.cellText(this._x, this._y, text);
    this._text = text;
  }
}
