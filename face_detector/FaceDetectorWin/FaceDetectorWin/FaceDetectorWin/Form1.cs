using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Timers;
using System.Windows.Forms;

namespace FaceDetectorWin
{
    public partial class Form1 : Form
    {
        //Ran on start
        public Form1()
        {
            InitializeComponent();
            
        }
        //Code ran when button is clicked
        private void startBt_Click(object sender, EventArgs e)
        {
            cmdCommand();
            InitTimer();
        }
        //Create timer and method to start it
        private System.Timers.Timer timer1;
        public void InitTimer()
        {
            timer1 = new System.Timers.Timer();
            timer1.Elapsed += new ElapsedEventHandler(timer1_Tick);
            timer1.Interval = 100; // in miliseconds
            timer1.Start();
        }
        //Process to start python and script when button is clicked
        public void cmdCommand()
        {
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.WindowStyle = ProcessWindowStyle.Hidden;
            startInfo.FileName = @"" + comboBox1.Text;
            startInfo.Arguments = @"camera_object_mono.py";
            Process process = new Process();
            process.StartInfo = startInfo;
            process.Start();

        }
        //Method ran everytime the timer is triggered 
        private void timer1_Tick(object sender, EventArgs e)
        {
            try
            {
                var buffer = File.ReadAllBytes("1.png");
                //pictureBox1.Image = BytesToBitmap(buffer);
                pictureBox1.Image = ByteToImage(buffer);   
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error {0} Error on image update", ex);
            }

        }
        //Test method created to resolve flicker but failed
        public static Bitmap ByteToImage(byte[] blob)
        {
            MemoryStream mStream = new MemoryStream();
            byte[] pData = blob;
            mStream.Write(pData, 0, Convert.ToInt32(pData.Length));
            Bitmap bm = new Bitmap(mStream, false);
            mStream.Dispose();
            return bm;
        }
        
        //Method ran if the stop button is clicked 
        //Which kills the timer and the python script process
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
