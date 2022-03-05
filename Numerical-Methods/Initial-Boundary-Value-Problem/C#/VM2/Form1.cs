using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows.Forms.DataVisualization.Charting;

namespace VM2
{
    public partial class Form1 : Form
    {
        double[,] a_res;
        double[,] b_res;
        double L, T,  t, h, b0, b1, b2, fi1, fi2;

        int count_h, count_t;
        int task_number_a_or_b;

        double time_a, time_b;

        public Form1()
        {
            InitializeComponent();
            ChartArea chart = chart1.ChartAreas[0];
            chart.AxisX.RoundAxisValues();
            progressBar1.Minimum = 0;
            progressBar1.Value = 0;
            progressBar1.Step = 1;
        }

        private void TextBoxesDouble_TextFormat(object sender, KeyPressEventArgs e)
        {
            if (!((e.KeyChar >= '0' && e.KeyChar <= '9')
            || e.KeyChar == ',' || e.KeyChar == '.' || e.KeyChar == 8 || e.KeyChar == '-'))
            {
                e.Handled = true;
                return;
            }
            if (e.KeyChar == '.')
            {
                e.KeyChar = ',';
            }
        }

        private void TextBoxesInt_TextFormat(object sender, KeyPressEventArgs e)
        {
            ////if (!((e.KeyChar >= '0' && e.KeyChar <= '9')
            ////  || e.KeyChar == 8))
            ////{
            ////  e.Handled = true;
            ////  return;
            ////}
            if (!((e.KeyChar >= '0' && e.KeyChar <= '9')
            || e.KeyChar == ',' || e.KeyChar == '.' || e.KeyChar == 8 || e.KeyChar == '-'))
            {
                e.Handled = true;
                return;
            }
            if (e.KeyChar == '.')
            {
                e.KeyChar = ',';
            }
        }

        private void Form1_KeyUp(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                e.Handled = true;
                SelectNextControl(ActiveControl, true, true, true, true);
            }
        }

        // part A run
        private void button2_Click(object sender, EventArgs e)
        {
            if (label12.Text == "-")
            {
                MessageBox.Show("Действие возможно после нажатия кнопки 'Часть В'");
                return;
            }
            string part_a = "Результат А";
            if (chart1.Series[part_a].Enabled == false)
            {
                progressBar1.Value = 0;
                a_res = new double[count_h, count_t];
                task_number_a_or_b = 0;
                backgroundWorker1.RunWorkerAsync();
            }
        }

        private void label5_Click(object sender, EventArgs e){}
        private void label1_Click(object sender, EventArgs e) {}
        private void label13_Click(object sender, EventArgs e) {}
        private void groupBox1_Enter(object sender, EventArgs e) {}
        private void label16_Click(object sender, EventArgs e) {}


        private void Button1_Click(object sender, EventArgs e)
        {
            if(backgroundWorker1.IsBusy != true)
            {
                label10.Text = "-";
                label12.Text = "-";

                progressBar1.Value = 0;
                chart1.Series.Clear();
                chart1.Legends.Clear();

                L = double.Parse(textBox1.Text);
                T = double.Parse(textBox2.Text);
                t = double.Parse(textBox3.Text);
                h = double.Parse(textBox4.Text);
                fi1 = double.Parse(textBox5.Text);
                fi2 = double.Parse(textBox6.Text);
                b0 = double.Parse(textBox7.Text);
                b1 = double.Parse(textBox8.Text);
                b2 = double.Parse(textBox9.Text);
                count_h = (int)(1 + L / h);
                count_t = (int)(1 + T / t);
                //if (t / (h * h) < 1.0 / 4)
                //{
                //  MessageBox.Show("Условие устойчивости не доказано.\n(a^2t)/h^2 < 1/4 (а=1)\n" +
                //                  "t/h^2= "+ t / (h * h));
                //  return;
                //}
                chart1.ChartAreas[0].AxisX.Minimum = 0;
                chart1.ChartAreas[0].AxisX.Maximum = L;
                b_res = new double[count_h, count_t];

                progressBar1.Maximum = count_t;

                task_number_a_or_b = 1;
                backgroundWorker1.RunWorkerAsync();
            }
        }

        private void BackgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            BackgroundWorker worker = sender as BackgroundWorker;


            if (task_number_a_or_b == 1)
                b_res = GetResult();
            else
                a_res = GetResult();
        }

        private void BackgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            if (task_number_a_or_b == 1)
            {
                Task_B();
                label12.Text = (time_b).ToString();
            }
            else
            {
                Task_A();
                label10.Text = (time_a).ToString();
            }
        }

        private double phi(double x)
        {
            return (1.0 / L) + fi1 * Math.Cos((Math.PI * x) / L) + fi2 * Math.Cos((2 * Math.PI * x) / L);
        }

        public double b(double x)
        {
            return task_number_a_or_b * b0 + b1 * Math.Cos((Math.PI * x) / L) + b2 * Math.Cos((2 * Math.PI * x) / L);
        }

        private double Simpson_method(ref double[,] result, int tstep, int task_name)
        {
            int kf;
            double intergral;
            double cx = h;

            if (task_name == 1)
            {
                intergral = b(0) * result[0, tstep];
                for (int i = 1; i < count_h - 1; ++i)
                {
                kf = 4;
                if (i % 2 == 0) kf = 2;
                intergral += b(cx) * kf * result[i, tstep];
                cx += h;
                }
                intergral += b(cx) * result[count_h - 1, tstep];
            }
            else
            {
                intergral = result[0, tstep];
                for (int i = 1; i < count_h - 1; i++)
                {
                kf = 4;
                if (i % 2 == 0) kf = 2;
                intergral += kf * result[i, tstep];
                cx += h;
                }
                intergral += result[count_h - 1, tstep];
            }
            intergral *= (h / 3);
            return intergral;
        }

        private double[] Fcount(ref double[,] result, int tstep, int part)
        {
            double[] F = new double[count_h];
            for (int i = 0; i < count_h; i++)
                F[i] = h * h * result[i, tstep] * (t * (b(h * i) - part * Simpson_method(ref result, tstep, part)) + 1);
            return F;
        }

        public double[,] GetResult()
        {
            double[] F;
            double[] alpha = new double[count_h];
            double[] beta = new double[count_h];
            double[,] result = new double[count_h, count_t];

            var timer = System.Diagnostics.Stopwatch.StartNew();

            double current_x = 0;
            for (int k = 0; k < count_h; k++)
            {
                result[k, 0] = phi(current_x);
                current_x += h;
            }

            int K = count_h;
            double B, C0, Ak, Ck, AK;
            B = h * h + 2 * t;
            C0 = AK = -2 * t;
            Ak = Ck = -1 * t;

            for (int t_st_id = 0; t_st_id < count_t - 1; t_st_id++)
            {
                F = Fcount(ref result, t_st_id, task_number_a_or_b);

                alpha[0] = -1 * (C0 / B);
                beta[0] = F[0] / B;

                for (int k = 1; k < K - 1; k++)
                {
                    alpha[k] = (-1 * Ck) / (Ak * alpha[k - 1] + B);
                    beta[k] = (F[k] - Ak * beta[k - 1]) / (Ak * alpha[k - 1] + B);
                }

                result[K - 1, t_st_id + 1] = (F[K - 1] - AK * beta[K - 2]) / (AK * alpha[K - 2] + B);

                for (int k = K - 1; k > 0; k--)
                {
                    result[k - 1, t_st_id + 1] = alpha[k - 1] * result[k, t_st_id + 1] + beta[k - 1];
                }

                // progressBar1.Value++;
                progressBar1.Invoke(new Action(() => progressBar1.Value++));
            }

            if (task_number_a_or_b == 0)
                {
                double I = Simpson_method(ref result, count_t - 1, 0);
                for (int k = 0; k < K; k++)
                    result[k, count_t - 1] /= I;
            }

            timer.Stop();
            double time = (timer.Elapsed).TotalMilliseconds;
            if (task_number_a_or_b == 0) time_a = time;
            else time_b = time;

            return result;
        }

        private void Task_A()
        {
            progressBar1.Value = count_t;

            string part_a = "Результат А";
            chart1.Series[part_a].Enabled = true;
            chart1.Series[part_a].IsVisibleInLegend = true;

            double current_x = 0;
            for (int k = 0; k < count_h; ++k)
            {
                chart1.Series[part_a].Points.AddXY(current_x, a_res[k, count_t - 1]);
                current_x += h;
            }
        }

        private void Task_B()
        {
            string end_t = "Результат В";
            string begin_t = "φ(x)";
            string part_a = "Результат А";

              chart1.Series.Add(begin_t);
              chart1.Series.Add(end_t);
              chart1.Series.Add(part_a);

              chart1.Series[begin_t].IsVisibleInLegend = true;
              chart1.Series[end_t].IsVisibleInLegend = true;
              chart1.Series[part_a].IsVisibleInLegend = false;

              chart1.Series[part_a].Enabled = false;

              chart1.Series[begin_t].ChartType = SeriesChartType.Spline;
              chart1.Series[end_t].ChartType = SeriesChartType.Spline;
              chart1.Series[part_a].ChartType = SeriesChartType.Spline;

              chart1.Series[begin_t].BorderWidth = 2;
              chart1.Series[end_t].BorderWidth = 2;
              chart1.Series[part_a].BorderWidth = 2;

              chart1.Series[begin_t].Color = Color.DarkBlue;
              chart1.Series[end_t].Color = Color.Tomato;
              chart1.Series[part_a].Color = Color.LightGreen;

              chart1.Legends.Add(new Legend("legend"));
              chart1.Legends["legend"].Font = new Font(chart1.Legends["legend"].Font.FontFamily, 10);
              chart1.Legends["legend"].Docking = Docking.Bottom;
              chart1.Legends["legend"].LegendStyle = LegendStyle.Column;

            double current_x = 0;
            for (int k = 0; k < count_h; k++)
            {
                chart1.Series[begin_t].Points.AddXY(current_x, b_res[k, 0]);
                chart1.Series[end_t].Points.AddXY(current_x, b_res[k, count_t - 1]);
                current_x += h;
            }

              MyDataGrid.RowCount = count_h;
              MyDataGrid.ColumnCount = 2;
              MyDataGrid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
              MyDataGrid.Columns[0].HeaderText = "φ[i]";
              MyDataGrid.Columns[1].HeaderText = "b[i]";

            for (int k = 0; k < count_h; k++)
            {
                MyDataGrid.Rows[k].HeaderCell.Value = k.ToString();
                MyDataGrid.Rows[k].Cells[0].Value = b_res[k, 0].ToString();
                MyDataGrid.Rows[k].Cells[1].Value = b(h * k).ToString();
            }
            progressBar1.Value = count_t;
            }
        }
}
