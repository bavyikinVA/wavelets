using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using System.Drawing.Imaging;

namespace PicColorSetter
{
    public partial class Form1 : Form
    {
        OpenFileDialog oDlg;
        SaveFileDialog sDlg;
        Color color;
        int I = 0, J = 0;
        public Form1()
        {
            InitializeComponent();
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            //setting initial values

            SetStyle(ControlStyles.AllPaintingInWmPaint |
               ControlStyles.UserPaint |
               ControlStyles.DoubleBuffer,
               true);

            oDlg = new OpenFileDialog(); // Open Dialog Initialization
            oDlg.RestoreDirectory = true;
            oDlg.InitialDirectory = "C:\\";
            oDlg.FilterIndex = 1;
            oDlg.Filter = "jpg Files (*.jpg)|*.jpg|gif Files (*.gif)|*.gif|png Files (*.png)|*.png |bmp Files (*.bmp)|*.bmp";
            /*************************/
            sDlg = new SaveFileDialog(); // Save Dialog Initialization
            sDlg.RestoreDirectory = true;
            sDlg.InitialDirectory = "C:\\";
            sDlg.FilterIndex = 5;
            sDlg.Filter = "txt Files (*.txt)| *.txt";
            /*************************/

            RedSelection.Value = 128;
            GreenSelection.Value = 128;
            BlueSelection.Value = 128;
            BrightnessSelection.Value = 128;
            SelectedColor.BackColor = Color.FromArgb(RedSelection.Value, GreenSelection.Value, BlueSelection.Value);
            //ColorPictur();
        }
        private void scrColorComponent_Scroll(object sender, ScrollEventArgs e)
        {
            //redrawing & adjusting the selected color
            SelectedColor.BackColor = Color.FromArgb(RedSelection.Value, GreenSelection.Value, BlueSelection.Value);
            ColorPictur();
        }
        private void ColorPictur()
        {
            //applyig color
            picToned.Image = ToColorTone(picOriginal.Image, SelectedColor.BackColor);
        }
        private Bitmap ToColorTone(Image image, Color color)
        {
            //creating a new bitmap image with selected color.
            float scale = BrightnessSelection.Value / 128f;

            float r = color.R / 255f * scale;
            float g = color.G / 255f * scale;
            float b = color.B / 255f * scale;

            // Color Matrix
            ColorMatrix cm = new ColorMatrix(new float[][]
            {
                new float[] {r, 0, 0, 0, 0},
                new float[] {0, g, 0, 0, 0},
                new float[] {0, 0, b, 0, 0},
                new float[] {0, 0, 0, 1, 0},
                new float[] {0, 0, 0, 0, 1}
            });
            ImageAttributes ImAttribute = new ImageAttributes();
            ImAttribute.SetColorMatrix(cm);

            //Color Matrix on new bitmap image
            Point[] points =
            {
                new Point(0, 0),
                new Point(image.Width - 1, 0),
                new Point(0, image.Height - 1),
            };
            Rectangle rect = new Rectangle(0, 0, image.Width, image.Height);

            Bitmap myBitmap = new Bitmap(image.Width, image.Height);
            using (Graphics graphics = Graphics.FromImage(myBitmap))
            {
                graphics.DrawImage(image, points, rect, GraphicsUnit.Pixel, ImAttribute);
            }
            return myBitmap;
        }

        private void SavePicBtn_Click(object sender, EventArgs e)
        {
            sDlg.CheckFileExists = false;
            sDlg.CheckPathExists = true;
            Bitmap bmp = new Bitmap(picToned.Image);
            sDlg.FileName = "C:\\Red.txt";
            StringBuilder sbRed = new StringBuilder("");
            StringBuilder sbGreen = new StringBuilder("");
            StringBuilder sbBlue = new StringBuilder("");
            StringBuilder sbBrightness = new StringBuilder("");
            StringBuilder sbContrast = new StringBuilder("");
            StringBuilder sbContrastExt = new StringBuilder("");

            for (int i = 0; i < bmp.Height; i++)
                {
                    for (int j = 0; j < bmp.Width; j++)
                    {
                        Color clr = bmp.GetPixel(j, i);
                        double brightness = clr.R + clr.G + clr.B;
                        sbRed.Append(clr.R.ToString() + " ");
                        sbGreen.Append(clr.G.ToString() + " ");
                        sbBlue.Append(clr.B.ToString() + " ");
                        sbBrightness.Append(brightness.ToString() + " ");
                        double contrast = 0;
                        if (j != bmp.Width - 1)
                        {
                            Color clr1 = bmp.GetPixel(j+1, i);
                            contrast = brightness - clr1.R - clr1.G - clr1.B;
                        }
                        sbContrast.Append(contrast.ToString() + " ");
                    }
                    sbRed.AppendLine("\n");
                    sbGreen.AppendLine("\n");
                    sbBlue.AppendLine("\n");
                    sbBrightness.AppendLine("\n");
                    sbContrast.AppendLine("\n");
                }
            for (int i = 0; i < bmp.Width; i++)
            {
                for (int j = 0; j < bmp.Height; j++)
                {

                    Color clr = bmp.GetPixel(i, j);
                    double brightness = clr.R + clr.G + clr.B;
                    double contrast = 0;
                    if (j != bmp.Height - 1)
                    {
                        Color clr1 = bmp.GetPixel(i, j+1);
                        contrast = brightness - clr1.R - clr1.G - clr1.B;
                    }

                    sbContrastExt.Append(contrast.ToString() + " ");

                }
                sbContrastExt.AppendLine("\n");
            }
            if (sDlg.ShowDialog(this) == DialogResult.OK)
                {
                    File.WriteAllText(sDlg.FileName, sbRed.ToString());
                    String directory = Path.GetDirectoryName(sDlg.FileName);
                    StreamWriter swGreen = new StreamWriter(directory + "\\Green.txt");
                    StreamWriter swBlue = new StreamWriter(directory + "\\Blue.txt");
                    StreamWriter swBrightness = new StreamWriter(directory + "\\Brightness.txt");
                    StreamWriter swContrast = new StreamWriter(directory + "\\Contrast_vertical.txt");
                    StreamWriter swContrastExtended = new StreamWriter(directory + "\\Contrast_horizontal.txt");
                    swGreen.Write(sbGreen.ToString());
                    swBlue.Write(sbBlue.ToString());
                    swBrightness.Write(sbBrightness.ToString());
                    swContrast.Write(sbContrast.ToString());
                    swContrastExtended.Write(sbContrastExt.ToString());
                    swGreen.Close();
                    swBlue.Close();
                    swBrightness.Close();
                    swContrast.Close();
                    swContrastExtended.Close();
                }
            


            }

            private void picOriginal_Click(object sender, EventArgs e)
        {


        }

        private void OpenPicBtn_Click(object sender, EventArgs e)
        {
            //string filepath = @"D:\";

            oDlg.Filter = "jpg Files (*.jpg)|*.jpg|gif Files (*.gif)|*.gif|png Files (*.png)|*.png |bmp Files (*.bmp)|*.bmp";
            oDlg.CheckFileExists = true;
            oDlg.CheckPathExists = true;

            if (oDlg.ShowDialog(this) == DialogResult.OK)
            {
                try
                {
                    string filename = oDlg.FileName;
                    FileStream fs = new FileStream(filename, FileMode.Open, FileAccess.Read); //set file stream
                    Byte[] bindata = new byte[Convert.ToInt32(fs.Length)];
                    fs.Read(bindata, 0, Convert.ToInt32(fs.Length));
                    MemoryStream stream = new MemoryStream(bindata);//load picture 
                    stream.Position = 0;
                    picOriginal.Image = Image.FromStream(stream);
                    picToned.Image = Image.FromStream(stream);

                }
                catch
                {
                    MessageBox.Show("Wrong file!");
                }

            }
        }

        private void picToned_MouseClick(object sender, MouseEventArgs e)
        {
     
        }

        private void picToned_Click(object sender, EventArgs e)
        {
            
            var mouseEventArgs = e as MouseEventArgs;
            if (mouseEventArgs != null)
            {
                Bitmap bmp = new Bitmap(picToned.Image);
                I = mouseEventArgs.Y;
                J = mouseEventArgs.X;
                Color clr = bmp.GetPixel(mouseEventArgs.X, mouseEventArgs.Y);
                label8.Text = clr.R.ToString();
                label9.Text = clr.G.ToString();
                label10.Text = clr.B.ToString(); 
                double br = clr.R + clr.G + clr.B;
                label12.Text = br.ToString();
                Color clr1 = bmp.GetPixel(mouseEventArgs.X + 1, mouseEventArgs.Y);
                double cn = clr.R + clr.G +  clr.B - (clr1.R + clr1.G + clr1.B);
                label11.Text = cn.ToString();
            }
        }

        private void groupBox4_Enter(object sender, EventArgs e)
        {

        }

        private void label12_Click(object sender, EventArgs e)
        {

        }

        private void label11_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            {
                sDlg.CheckFileExists = false;
                sDlg.CheckPathExists = true;
                Bitmap bmp = new Bitmap(picToned.Image);
                sDlg.FileName = "C:\\Red(Width).txt";
                StringBuilder sbRed = new StringBuilder("");
                StringBuilder sbGreen = new StringBuilder("");
                StringBuilder sbBlue = new StringBuilder("");
                StringBuilder sbBrightness = new StringBuilder("");
                StringBuilder sbContrast = new StringBuilder("");

                for (int i = 0; i < bmp.Width; i++)
                {
                    Color clr = bmp.GetPixel(i, I);
                    double brightness = clr.R + clr.G + clr.B;
                    sbRed.Append(clr.R.ToString() + " ");
                    sbGreen.Append(clr.G.ToString() + " ");
                    sbBlue.Append(clr.B.ToString() + " ");
                    sbBrightness.Append(brightness.ToString() + " ");
                    double contrast = 0;
                    if (i != bmp.Width - 1)
                    {
                        Color clr1 = bmp.GetPixel(i+1, I);
                        contrast = brightness - clr1.R - clr1.G - clr1.B;
                    }

                    sbContrast.Append(contrast.ToString() + " ");

                }

                if (sDlg.ShowDialog(this) == DialogResult.OK)
                {
                    File.WriteAllText(sDlg.FileName, sbRed.ToString());
                    String directory = Path.GetDirectoryName(sDlg.FileName);
                    StreamWriter swGreen = new StreamWriter(directory + "\\Green(Width).txt");
                    StreamWriter swBlue = new StreamWriter(directory + "\\Blue(Width).txt");
                    StreamWriter swBrightness = new StreamWriter(directory + "\\Brightness(Width).txt");
                    StreamWriter swContrast = new StreamWriter(directory + "\\Contrast(Width).txt");
                    swGreen.Write(sbGreen.ToString());
                    swBlue.Write(sbBlue.ToString());
                    swBrightness.Write(sbBrightness.ToString());
                    swContrast.Write(sbContrast.ToString());
                    swGreen.Close();
                    swBlue.Close();
                    swBrightness.Close();
                    swContrast.Close();
                }



            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            sDlg.CheckFileExists = false;
            sDlg.CheckPathExists = true;
            Bitmap bmp = new Bitmap(picToned.Image);
            sDlg.FileName = "C:\\Red(Height).txt";
            StringBuilder sbRed = new StringBuilder("");
            StringBuilder sbGreen = new StringBuilder("");
            StringBuilder sbBlue = new StringBuilder("");
            StringBuilder sbBrightness = new StringBuilder("");
            StringBuilder sbContrast = new StringBuilder("");

            for (int i = 0; i < bmp.Height; i++)
            {
                Color clr = bmp.GetPixel(J, i);
                double brightness = clr.R + clr.G + clr.B;
                sbRed.Append(clr.R.ToString() + " ");
                sbGreen.Append(clr.G.ToString() + " ");
                sbBlue.Append(clr.B.ToString() + " ");
                sbBrightness.Append(brightness.ToString() + " ");
                double contrast = 0;
                if (i != bmp.Height - 1)
                {
                    Color clr1 = bmp.GetPixel(J, i + 1);
                    contrast = brightness - clr1.R - clr1.G - clr1.B;
                }
                sbContrast.Append(contrast.ToString() + " ");
            }
            
            if (sDlg.ShowDialog(this) == DialogResult.OK)
            {
                File.WriteAllText(sDlg.FileName, sbRed.ToString());
                String directory = Path.GetDirectoryName(sDlg.FileName);
                //label10.Text = directory;
                // StreamWriter swRed = new StreamWriter("D:\\Red.txt");
                StreamWriter swGreen = new StreamWriter(directory + "\\Green(Height).txt");
                StreamWriter swBlue = new StreamWriter(directory + "\\Blue(Height).txt");
                StreamWriter swBrightness = new StreamWriter(directory + "\\Brightness(Height).txt");
                StreamWriter swContrast = new StreamWriter(directory + "\\Contrast(Height).txt");
                swGreen.Write(sbGreen.ToString());
                swBlue.Write(sbBlue.ToString());
                swBrightness.Write(sbBrightness.ToString());
                swContrast.Write(sbContrast.ToString());
                swGreen.Close();
                swBlue.Close();
                swBrightness.Close();
                swContrast.Close();
            }
        }
    }
}
