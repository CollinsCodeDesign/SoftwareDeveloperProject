using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Timers;
using System.IO;
using System.Diagnostics;
using Xunit;

namespace FaceDetectorWin
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void startBt_Click(object sender, EventArgs e)
        {
            cmdCommand();
            InitTimer();
        }
        private System.Timers.Timer timer1;
        public void InitTimer()
        {
            timer1 = new System.Timers.Timer();
            timer1.Elapsed += new ElapsedEventHandler(timer1_Tick);
            timer1.Interval = 60; // in miliseconds
            timer1.Start();
        }
        public void cmdCommand()
        {
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = @"C:\Users\chris\AppData\Local\Programs\Thonny\python.exe";
            startInfo.Arguments = @"camera_object_mono.py";
            Process process = new Process();
            process.StartInfo = startInfo;
            process.Start();

        }
        private void timer1_Tick(object sender, EventArgs e)
        {
            try
            {
                if (pictureBox1.Image != null)
                {
                    pictureBox1.Image = null;
                }
                else
                {
                    var buffer = File.ReadAllBytes("1.png");
                    pictureBox1.Image = ByteToImage(buffer);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error {0} Error on image update", ex);
            }

        }
        public static Bitmap ByteToImage(byte[] blob)
        {
            MemoryStream mStream = new MemoryStream();
            byte[] pData = blob;
            mStream.Write(pData, 0, Convert.ToInt32(pData.Length));
            Bitmap bm = new Bitmap(mStream, false);
            mStream.Dispose();
            return bm;
        }
        private void stopBt_Click(object sender, EventArgs e)
        {
            timer1.Stop();
            foreach (var process in Process.GetProcessesByName("python"))
            {
                process.Kill();
            }
        }
    }
}
