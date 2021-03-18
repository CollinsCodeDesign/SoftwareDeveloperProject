using System;
using System.IO;
using System.Diagnostics;
using System.Timers;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Gtk;

public partial class MainWindow : Gtk.Window
{
    bool killScript = false;
    public MainWindow() : base(Gtk.WindowType.Toplevel)
    {
        Build();
        Item item = JsonConvert.DeserializeObject<Item>(LoadJson().ToString());
        faceEntry.Text = item.face_xml_cascade;
        eyeEntry.Text = item.eye_xml_cascade;
        smileEntry.Text = item.smile_xml_cascade;
        FColorEntry.Text = item.face_box_color;
        EColorEntry.Text = item.eye_box_color;
        SColorEntry.Text = item.smile_box_color;
        FLbColorEntry.Text = item.color_of_face_label;
        ELbColorEntry.Text = item.color_of_eye_label;
        SLbColorEntry.Text = item.color_of_smile_label;
        notebook1.Page = 0;
        var buffer = System.IO.File.ReadAllBytes("1.png");
        var pixbuf = new Gdk.Pixbuf(buffer);
        image1.Pixbuf = pixbuf;
    }

    protected void OnDeleteEvent(object sender, DeleteEventArgs a)
    {
        ExecuteBashCommand("kill $(cat camera_pid)");
        Application.Quit();
        a.RetVal = true;
    }

    protected void startBt(object sender, EventArgs e)
    {
        ExecuteBashCommand("python3 camera_object_mono.py & echo $! > camera_pid");
        InitTimer();
        killScript = true;
    }
    static void ExecuteBashCommand(string command)
    {
        command = command.Replace("\"", "\"\"");

        var proc = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "/bin/bash",
                Arguments = "-c \"" + command + "\"",
                UseShellExecute = false
            }
        };

        proc.Start();
    }
    private Timer timer1;
    public void InitTimer()
    {
        timer1 = new Timer();
        timer1.Elapsed += new ElapsedEventHandler(timer1_Tick);
        timer1.Interval = 60; // in miliseconds
        timer1.Start();
    }

    private void timer1_Tick(object sender, EventArgs e)
    {
        try
        {
            image1.Pixbuf = null;
            var buffer = System.IO.File.ReadAllBytes("1.png");
            var pixbuf = new Gdk.Pixbuf(buffer);
            image1.Pixbuf = pixbuf;
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error {0} Error on image update", ex);
        }

    }

    protected void PageSwitch(object o, SwitchPageArgs args)
    {
        if (killScript)
        {
            ExecuteBashCommand("kill $(cat camera_pid)");
            timer1.Stop();
            killScript = false;
        }
        setJson();
        ExecuteBashCommand("cp face_detector_config1.json face_detector_config.json");
    }

    protected void stopBt(object sender, EventArgs e)
    {
        if (killScript)
        {
            ExecuteBashCommand("kill $(cat camera_pid)");
            timer1.Stop();
            killScript = false;
        }
    }
    public object LoadJson()
    {
        using (StreamReader r = new StreamReader("face_detector_config.json"))
        {
            var serializer = new JsonSerializer();
            using (var sr = new StreamReader(r.BaseStream))
            using (var jsonTextReader = new JsonTextReader(sr))
            {
                return serializer.Deserialize(jsonTextReader);
            }
        }
    }

    public class Item
    {
        public string camera_input_info;
        public int camera_input;
        public string face_xml_cascade;
        public string eye_xml_cascade;
        public string smile_xml_cascade;
        public string face_box_color;
        public string eye_box_color;
        public string smile_box_color;
        public string font_size_of_label;
        public string font_thickness_of_label;
        public string color_of_face_label;
        public string color_of_eye_label;
        public string color_of_smile_label;
        public string line_thickness_of_boxes;

    }
    public void setJson()
    {
        string filepath = "face_detector_config.json";
        string result = string.Empty;
        using (StreamReader r = new StreamReader(filepath))
        {
            var json = r.ReadToEnd();
            var job = JObject.Parse(json);

            foreach (var item in job.Properties())
            {
                if (item.Name.Equals("face_xml_cascade"))
                {
                    item.Value = faceEntry.Text;
                }
                else if (item.Name.Equals("eye_xml_cascade"))
                {
                    item.Value = eyeEntry.Text;
                }
                else if (item.Name.Equals("smile_xml_cascade"))
                {
                    item.Value = smileEntry.Text;
                }
                else if (item.Name.Equals("face_box_color"))
                {
                    item.Value = FColorEntry.Text;
                }
                else if (item.Name.Equals("eye_box_color"))
                {
                    item.Value = EColorEntry.Text;
                }
                else if (item.Name.Equals("smile_box_color"))
                {
                    item.Value = SColorEntry.Text;
                }
                else if (item.Name.Equals("color_of_face_label"))
                {
                    item.Value = FLbColorEntry.Text;
                }
                else if (item.Name.Equals("color_of_eye_label"))
                {
                    item.Value = ELbColorEntry.Text;
                }
                else if (item.Name.Equals("color_of_smile_label"))
                {
                    item.Value = SLbColorEntry.Text;
                }

                result = job.ToString();
            }

            File.WriteAllText("face_detector_config1.json", result);
        }
    }
}
