using System;
using System.Drawing;
using System.Windows.Forms;
using System.Threading.Tasks;

namespace TicTacToe
{
    public partial class Form1 : Form
    {
        private bool isPlayerX = true;
        private int moveCount = 0;
        private int scoreX = 0;
        private int scoreO = 0;
        private int draws = 0;
        private Button[,] buttons;
        private bool gameFinished = false;
        private Label lblStatus;
        private Label lblScore;
        private Button btnNewGame;
        private TableLayoutPanel mainTable;

        public Form1()
        {
            InitializeComponent();
            SetupForm();
            CreateGameBoard();
            InitializeGame();
        }

        private void SetupForm()
        {
            this.Text = "Крестики-Нолики";
            this.Size = new Size(500, 550);
            this.MinimumSize = new Size(400, 450);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.BackColor = Color.White;
        }

        private void CreateGameBoard()
        {
            // Создаем главную таблицу
            mainTable = new TableLayoutPanel();
            mainTable.RowCount = 4;
            mainTable.ColumnCount = 3;
            mainTable.Dock = DockStyle.Fill;
            mainTable.BackColor = Color.White;

            // Настройка строк
            for (int i = 0; i < 3; i++)
            {
                mainTable.RowStyles.Add(new RowStyle(SizeType.Percent, 33.33F));
            }
            mainTable.RowStyles.Add(new RowStyle(SizeType.Absolute, 100F));

            // Настройка колонок
            for (int i = 0; i < 3; i++)
            {
                mainTable.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 33.33F));
            }

            // Создаем массив кнопок
            buttons = new Button[3, 3];

            // Создаем кнопки игрового поля
            for (int row = 0; row < 3; row++)
            {
                for (int col = 0; col < 3; col++)
                {
                    buttons[row, col] = new Button();
                    buttons[row, col].Name = $"btn_{row}_{col}";
                    buttons[row, col].Text = "";
                    buttons[row, col].Font = new Font("Arial", 32, FontStyle.Bold);
                    buttons[row, col].Dock = DockStyle.Fill;
                    buttons[row, col].Margin = new Padding(5);
                    buttons[row, col].BackColor = Color.White;
                    buttons[row, col].FlatStyle = FlatStyle.Flat;

                    // Стиль для плоской кнопки
                    buttons[row, col].FlatAppearance.BorderColor = Color.LightGray;
                    buttons[row, col].FlatAppearance.BorderSize = 2;

                    // Обработчик клика
                    buttons[row, col].Click += new EventHandler(Button_Click);

                    mainTable.Controls.Add(buttons[row, col], col, row);
                }
            }

            // Создаем панель для управления
            Panel controlPanel = new Panel();
            controlPanel.Dock = DockStyle.Fill;
            controlPanel.BackColor = Color.AliceBlue;

            // Добавляем Label для статуса
            lblStatus = new Label();
            lblStatus.Text = "Сейчас ходит: X";
            lblStatus.Font = new Font("Arial", 14, FontStyle.Bold);
            lblStatus.ForeColor = Color.Red;
            lblStatus.TextAlign = ContentAlignment.MiddleCenter;
            lblStatus.Dock = DockStyle.Top;
            lblStatus.Height = 40;
            lblStatus.Margin = new Padding(0, 10, 0, 0);

            // Добавляем Label для счета
            lblScore = new Label();
            lblScore.Text = "Счет: X - 0 | O - 0 | Ничьи: 0";
            lblScore.Font = new Font("Arial", 10);
            lblScore.TextAlign = ContentAlignment.MiddleCenter;
            lblScore.Dock = DockStyle.Top;
            lblScore.Height = 30;
            lblScore.Margin = new Padding(0, 5, 0, 0);

            // Добавляем кнопку новой игры
            btnNewGame = new Button();
            btnNewGame.Text = "Новая игра";
            btnNewGame.Font = new Font("Arial", 12, FontStyle.Bold);
            btnNewGame.Dock = DockStyle.Bottom;
            btnNewGame.Height = 40;
            btnNewGame.Margin = new Padding(100, 10, 100, 10);
            btnNewGame.BackColor = Color.LightGreen;
            btnNewGame.FlatStyle = FlatStyle.Flat;

            btnNewGame.FlatAppearance.BorderColor = Color.Green;
            btnNewGame.FlatAppearance.BorderSize = 1;
            btnNewGame.Click += new EventHandler(btnNewGame_Click);

            // Добавляем элементы на панель управления
            controlPanel.Controls.Add(lblStatus);
            controlPanel.Controls.Add(lblScore);
            controlPanel.Controls.Add(btnNewGame);

            // Добавляем панель управления в таблицу
            mainTable.Controls.Add(controlPanel, 0, 3);
            mainTable.SetColumnSpan(controlPanel, 3);

            // Добавляем таблицу на форму
            this.Controls.Add(mainTable);
        }

        private void InitializeGame()
        {
            // Сброс всех кнопок
            for (int row = 0; row < 3; row++)
            {
                for (int col = 0; col < 3; col++)
                {
                    buttons[row, col].Text = "";
                    buttons[row, col].Enabled = true;
                    buttons[row, col].BackColor = Color.White;
                    buttons[row, col].ForeColor = Color.Black;
                }
            }

            isPlayerX = true;
            moveCount = 0;
            gameFinished = false;
            UpdateStatus();
        }

        private void Button_Click(object sender, EventArgs e)
        {
            if (gameFinished) return;

            Button button = (Button)sender;

            if (button.Text != "") return;

            // Устанавливаем символ текущего игрока
            if (isPlayerX)
            {
                button.Text = "X";
                button.ForeColor = Color.Red;
            }
            else
            {
                button.Text = "O";
                button.ForeColor = Color.Blue;
            }

            moveCount++;

            // Проверка на победу
            if (CheckForWin())
            {
                gameFinished = true;
                HighlightWinningLine();
                if (isPlayerX)
                {
                    scoreX++;
                    ShowWinMessage("Игрок X победил!", Color.Red);
                }
                else
                {
                    scoreO++;
                    ShowWinMessage("Игрок O победил!", Color.Blue);
                }
                UpdateStatus();
                return;
            }

            // Проверка на ничью
            if (moveCount == 9)
            {
                gameFinished = true;
                draws++;
                ShowDrawMessage();
                UpdateStatus();
                return;
            }

            // Смена игрока
            isPlayerX = !isPlayerX;
            UpdateStatus();
        }

        private bool CheckForWin()
        {
            string currentSymbol = isPlayerX ? "X" : "O";

            // Проверка горизонталей
            for (int row = 0; row < 3; row++)
            {
                if (buttons[row, 0].Text == currentSymbol &&
                    buttons[row, 1].Text == currentSymbol &&
                    buttons[row, 2].Text == currentSymbol)
                {
                    return true;
                }
            }

            // Проверка вертикалей
            for (int col = 0; col < 3; col++)
            {
                if (buttons[0, col].Text == currentSymbol &&
                    buttons[1, col].Text == currentSymbol &&
                    buttons[2, col].Text == currentSymbol)
                {
                    return true;
                }
            }

            // Проверка диагоналей
            if (buttons[0, 0].Text == currentSymbol &&
                buttons[1, 1].Text == currentSymbol &&
                buttons[2, 2].Text == currentSymbol)
            {
                return true;
            }

            if (buttons[0, 2].Text == currentSymbol &&
                buttons[1, 1].Text == currentSymbol &&
                buttons[2, 0].Text == currentSymbol)
            {
                return true;
            }

            return false;
        }

        private void HighlightWinningLine()
        {
            string currentSymbol = isPlayerX ? "X" : "O";
            Color winColor = isPlayerX ? Color.FromArgb(200, 255, 200) :
                                         Color.FromArgb(200, 200, 255);

            // Проверка горизонталей
            for (int row = 0; row < 3; row++)
            {
                if (buttons[row, 0].Text == currentSymbol &&
                    buttons[row, 1].Text == currentSymbol &&
                    buttons[row, 2].Text == currentSymbol)
                {
                    for (int col = 0; col < 3; col++)
                    {
                        buttons[row, col].BackColor = winColor;
                    }
                    return;
                }
            }

            // Проверка вертикалей
            for (int col = 0; col < 3; col++)
            {
                if (buttons[0, col].Text == currentSymbol &&
                    buttons[1, col].Text == currentSymbol &&
                    buttons[2, col].Text == currentSymbol)
                {
                    for (int row = 0; row < 3; row++)
                    {
                        buttons[row, col].BackColor = winColor;
                    }
                    return;
                }
            }

            // Проверка диагоналей
            if (buttons[0, 0].Text == currentSymbol &&
                buttons[1, 1].Text == currentSymbol &&
                buttons[2, 2].Text == currentSymbol)
            {
                buttons[0, 0].BackColor = winColor;
                buttons[1, 1].BackColor = winColor;
                buttons[2, 2].BackColor = winColor;
                return;
            }

            if (buttons[0, 2].Text == currentSymbol &&
                buttons[1, 1].Text == currentSymbol &&
                buttons[2, 0].Text == currentSymbol)
            {
                buttons[0, 2].BackColor = winColor;
                buttons[1, 1].BackColor = winColor;
                buttons[2, 0].BackColor = winColor;
            }
        }

        private void UpdateStatus()
        {
            if (!gameFinished)
            {
                if (isPlayerX)
                {
                    lblStatus.Text = "Сейчас ходит: X";
                    lblStatus.ForeColor = Color.Red;
                }
                else
                {
                    lblStatus.Text = "Сейчас ходит: O";
                    lblStatus.ForeColor = Color.Blue;
                }
            }
            else
            {
                lblStatus.Text = "Игра завершена";
                lblStatus.ForeColor = Color.Gray;
            }

            lblScore.Text = $"Счет: X - {scoreX} | O - {scoreO} | Ничьи: {draws}";
        }

        private void ShowWinMessage(string message, Color color)
        {
            lblStatus.Text = message;
            lblStatus.ForeColor = color;

            // Используем таймер для задержки перед показом MessageBox
            Timer timer = new Timer();
            timer.Interval = 100;
            timer.Tick += (s, args) =>
            {
                timer.Stop();
                MessageBox.Show(message, "Победа!",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            };
            timer.Start();
        }

        private void ShowDrawMessage()
        {
            lblStatus.Text = "Ничья!";
            lblStatus.ForeColor = Color.Gray;

            Timer timer = new Timer();
            timer.Interval = 100;
            timer.Tick += (s, args) =>
            {
                timer.Stop();
                MessageBox.Show("Ничья! Поле полностью заполнено.",
                    "Игра окончена", MessageBoxButtons.OK,
                    MessageBoxIcon.Information);
            };
            timer.Start();
        }

        private void btnNewGame_Click(object sender, EventArgs e)
        {
            InitializeGame();
        }

        protected override void OnResize(EventArgs e)
        {
            base.OnResize(e);
            // При изменении размера формы обновляем размер шрифта кнопок
            if (buttons != null)
            {
                int fontSize = Math.Max(20, Math.Min(40, this.Height / 15));
                foreach (Button btn in buttons)
                {
                    btn.Font = new Font("Arial", fontSize, FontStyle.Bold);
                }
            }
        }
    }
}