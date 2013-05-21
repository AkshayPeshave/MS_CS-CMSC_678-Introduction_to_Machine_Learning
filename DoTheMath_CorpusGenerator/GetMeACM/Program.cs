using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Xml.XPath;
using System.Collections;
using System.Net;
using System.IO;
using HtmlAgilityPack;
using System.Threading;
using System.Diagnostics;

namespace GetMeACM
{
    class Program
    {
        static void Main(string[] args)
        {
            //ExtractFromHTML metaExtractor = new ExtractFromHTML("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\HTML");
            //metaExtractor.ExtractMetadata();
            //ExtractFromPDF ccsExtractor = new ExtractFromPDF();
            //ccsExtractor.Extract();

            //getACMpages();
            //getACMPapers();

            //AlchemyAPIConnector.getConcepts("");

            //CreateLearningDataSet ds = new CreateLearningDataSet();
            //ds.ExtractUserKeyPhrases();

            //AlchemyAPIConnector.getConceptsFromKeywords();
            //extractContentFromPaperPDFs();

            //extractCCSClassification();

            CreateLearningDataSet ds = new CreateLearningDataSet();
            ds.ExtractCCSClassification();
        }

        //public static void ExtractPDFContent(string path)
        //{
        //    string pdfFilePath = path;
        //    java.io.BufferedWriter writer = new java.io.BufferedWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream("D:\\output.txt")));
        //    // get OutputTarget configured to pipe text to the provided file path
        //    OutputTarget tgt = new OutputTarget(writer);
        //    using (PDFTextStream pdfts = new PDFTextStream(pdfFilePath))
        //    {
        //        pdfts.pipe(tgt);
        //    }
        //    System.Console.WriteLine("The text extracted from {0} is:",
        //        pdfFilePath);
        //    //System.Console.WriteLine(tgt.);
        //}

        public static void getACMpages()
        {
            Random r = new Random(90);

            int next;
            StreamReader reader = new StreamReader("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\ACM Papers.txt");
            string acmId = reader.ReadLine();
            WebRequest req;
            FileStream f;
            int b;
            int count = 0;
            while (acmId != null)
            {
                //http://dl.acm.org/citation.cfm?id=2189816&CFID=315400250&CFTOKEN=59337421
                //http://dl.acm.org/citation.cfm?id=2189810&CFID=315400250&CFTOKEN=59337421
                req = HttpWebRequest.Create("http://dl.acm.org/citation.cfm?id=" + acmId);
                
                Stream str = req.GetResponse().GetResponseStream();

                Console.Write("\n"+ (++count) + ". " + acmId + ": Fetched... ");
                
                f = new FileStream("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\HTML\\" + acmId + ".htm", FileMode.Create);
                //f = new FileStream("D:\\" + acmId + ".htm", FileMode.Create);
                Console.WriteLine("Saving... ");

                while (true)
                {
                    b = str.ReadByte();
                    if (b == -1)
                        break;
                    else
                        f.WriteByte((byte)b);
                }

                Console.WriteLine("Saved... ");
                //HtmlWeb web = new HtmlWeb();
                //HtmlDocument doc = web.Load("http://dl.acm.org/citation.cfm?id=2189813&CFID=206048685&CFTOKEN=60919269");

                //byte[] byteStream = Encoding.UTF8.GetBytes(doc.DocumentNode.InnerHtml);
                //f.Write(byteStream, 0, byteStream.Length);

                next = r.Next(10, 150);
                Console.Write("Waiting "+ (next / 60) + " min...");
                System.Threading.Thread.Sleep(next * 1000);
                

                //break;

                acmId = reader.ReadLine();
            }
        }

        public static void getACMPapers()
        {
            Random r = new Random(90);

            int next;
            StreamReader reader = new StreamReader("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\ACM Papers.txt");
            string acmId = reader.ReadLine();
            HttpWebRequest req;
            FileStream f;
            int b;
            int count = 0;
            while (acmId != null)
            {
                //http://dl.acm.org/ft_gateway.cfm?id=1103968&type=pdf&coll=DL&dl=ACM&CFID=315400250&CFTOKEN=59337421
                req = (HttpWebRequest) HttpWebRequest.Create("http://dl.acm.org/ft_gateway.cfm?id=" + acmId + "&type=pdf&coll=DL&dl=ACM");
                req.AllowAutoRedirect = true;

                Stream str = req.GetResponse().GetResponseStream();

                Console.Write("\n" + (++count) + ". " + acmId + ": Fetched... ");

                //f = new FileStream("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\HTML\\" + acmId + ".htm", FileMode.Create);
                f = new FileStream("D:\\" + acmId + ".pdf", FileMode.Create);
                Console.WriteLine("Saving... ");

                while (true)
                {
                    b = str.ReadByte();
                    if (b == -1)
                        break;
                    else
                        f.WriteByte((byte)b);
                }

                Console.WriteLine("Saved... ");


                //next = r.Next(10, 150);
                //Console.Write("Waiting "+ (next / 60) + " min...");
                //Thread.Sleep(next * 1000);


                break;

                acmId = reader.ReadLine();
            }
        }

        public static void extractContentFromPaperPDFs()
        {
            PDFExtractor ext = new PDFExtractor();

            //StreamReader papers = new StreamReader("ACM Papers.txt");

            //string paper = papers.ReadLine();

            //while (paper != null)
            //{
            //    ext.ExtractPDFContent
            //        (@"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\PDF\" + paper + ".pdf",
            //        @"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\TEXT\" + paper + ".txt");

            //    paper = papers.ReadLine();
            //}

            ext.ExtractPDFContent
                    (@"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\PDF\1490273.pdf",
                    @"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\TEXT\1490273.txt");
        }

        public static void extractCCSClassification()
        {
            ExtractFromPaper ext = new ExtractFromPaper();

            StreamReader papers = new StreamReader("ACM Papers.txt");
            StringBuilder sb = new StringBuilder();

            string paper = papers.ReadLine();

            ArrayList ccs = new ArrayList();
            while (paper != null)
            {
                ccs = ext.ExtractCCS
                    (@"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\TEXT\" + paper + ".txt");
                string ccsLine = "";
                foreach (Object obj in ccs)
                {
                    ccsLine += (string)obj+",";
                }
                sb.AppendLine(ccsLine.Substring(0, ccsLine.Length - 1));
                paper = papers.ReadLine();
            }

            System.IO.File.WriteAllText("D:\\ccs.txt", sb.ToString());
        }
    }
}
