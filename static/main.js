

function gameEngine(myBoardID, opponentBoardID, infoSpaceID, settings) {
    var self = this;
    //var settings = {"cellCount": 10};

    function gameRender(gameBoard) {

        var ctx = gameBoard.getContext("2d");
        var cellBorderThickness = 1;
        var cellSize = gameBoard.width/settings.cellCount;
        var stepx = gameBoard.width/cellSize;
        var stepy = gameBoard.height/cellSize;

        this.drawCells = function(x,y) {
            for (var i = 0; i < gameBoard.width; i += cellSize) {
                ctx.beginPath();
                ctx.moveTo(i, 0);
                ctx.lineTo(i, gameBoard.height);
                ctx.lineWidth = cellBorderThickness;
                ctx.stroke();
            };
            for (var i = 0; i < gameBoard.height; i += cellSize) {
                ctx.beginPath();
                ctx.moveTo(0, i);
                ctx.lineTo(gameBoard.width, i);
                ctx.stroke();
            };

        };

        this.paintCell = function(col, row, color) {
           var size = cellSize - 2;
           var x = col * cellSize + 1;
           var y = row * cellSize + 1;
           ctx.fillStyle = color;
           ctx.fillRect(x, y, size, size);

        }

        this.init = function() {
            this.drawCells();
        }

    }


    function gameInput(gameBoard, CellClickCallback) {

        var cellSize = gameBoard.width/settings.cellCount;

        gameBoard.onclick = function(event) { 
            var rect = this.getBoundingClientRect();
            x = window.scrollX + event.clientX - rect.left;
            y = window.scrollY + event.clientY - rect.top;
            col = parseInt(x/cellSize);
            row = parseInt(y/cellSize);
            CellClickCallback(col, row);
        }; 
    }

    function gameNetwork(game, wsAddress) {

        var socket = new WebSocket(wsAddress);

        socket.onmessage = function(event) {
            var parsed_data = JSON.parse(event.data);
            switch (parsed_data[0]) {
            case settings.paintAction:
                game.color_cell(parsed_data[1], parsed_data[2], parsed_data[3], parsed_data[4]);
                break;
            case settings.setTextAction:
                game.set_text(parsed_data[1]);
                break;
            default:
                alert("wrong action " + parsed_data[0]);

            }
        };

        this.sendClickOnMyBoard = function(col, row) {
            var msg = JSON.stringify([settings.clickAction, settings.myBoardAction, col, row]);
            if (socket.readyState == 1) {
                socket.send(msg);
            }
        };

        this.sendClickOnOpponentBoard = function(col, row) {
            var msg = JSON.stringify([settings.clickAction, settings.opponentBoardAction, col, row]);
            if (socket.readyState == 1) {
                socket.send(msg);
            }
        };
    }






    var myBoard = document.getElementById(myBoardID);
    var opponentBoard = document.getElementById(opponentBoardID);
    var infoSpace = document.getElementById(infoSpaceID);
    var myRender = new gameRender(gameBoard);
    var opponentRender = new gameRender(opponentBoard);
    var network = new gameNetwork(self, settings.wsAddress);


    this.color_cell = function(board, color, col, row) {
        if (board == settings.myBoardAction) {
            myRender.paintCell(col, row, color);
        } else if (board == settings.opponentBoardAction) {
            opponentRender.paintCell(col, row, color);
        }
    };

    this.set_text = function(text) {
        infoSpace.innerHTML = text;
    }

    var myBoardInput = new gameInput(myBoard, network.sendClickOnMyBoard);
    var opponentBoardInput = new gameInput(opponentBoard, network.sendClickOnOpponentBoard);

    myRender.init();
    opponentRender.init();
}
