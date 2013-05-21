using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.IO;
using System.Collections;
using System.Net;
using System.Xml;
using System.Xml.XPath;


namespace GetMeACM
{
    class AlchemyAPIConnector
    {
        public static void getConcepts(string content)
        {
            WebRequest request = HttpWebRequest.Create("http://access.alchemyapi.com/calls/text/TextGetRankedConcepts?apikey=5b8a25eb136295b2185fd75187b0bacaf2a17f88");

            request.Method = "POST";
            string reqContent = "maxRetrieve=15&outputMode=rdf&text=" + content;

            StreamReader textFile = new StreamReader("D://output.txt");
            reqContent += textFile.ReadToEnd();

            // Convert POST data to a byte array.
            byte[] byteArray = Encoding.UTF8.GetBytes(reqContent);
            // Set the ContentType property of the WebRequest.
            request.ContentType = "application/x-www-form-urlencoded";
            // Set the ContentLength property of the WebRequest.
            request.ContentLength = byteArray.Length;
            // Get the request stream.
            Stream dataStream = request.GetRequestStream();
            // Write the data to the request stream.
            dataStream.Write(byteArray, 0, byteArray.Length);
            // Close the Stream object.
            dataStream.Close();

            WebResponse response = request.GetResponse();
            //Console.WriteLine(response.GetResponseStream().ToString());
            dataStream = response.GetResponseStream();

            FileStream f = new FileStream("D://responseXml.txt", FileMode.Create);
            int b = dataStream.ReadByte();
            while (b != -1)
            {
                f.WriteByte((byte)b);
                b = dataStream.ReadByte();
            }
        }


        public static void getConceptsFromKeywords()
        {
            WebRequest request = HttpWebRequest.Create("http://access.alchemyapi.com/calls/text/TextGetRankedKeywords?apikey=5b8a25eb136295b2185fd75187b0bacaf2a17f88&");

            request.Method = "POST";
            string reqContent = "maxRetrieve=15&outputMode=rdf&text=";

            StreamReader textFile = new StreamReader(@"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\ACM_meta.csv");


            string readLine = textFile.ReadLine();

            ArrayList keywords = new ArrayList();
            StringBuilder keywordsFile = new StringBuilder();

            while (readLine != null)
            {
                readLine=readLine.Split('\t')[4];
                readLine = readLine.Substring(1, readLine.Length - 2);
                request = HttpWebRequest.Create("http://access.alchemyapi.com/calls/text/TextGetRankedKeywords?apikey=5b8a25eb136295b2185fd75187b0bacaf2a17f88&");

                request.Method = "POST";
                
                reqContent = "maxRetrieve=15&outputMode=xml&text=" + readLine;
                // Convert POST data to a byte array.
                byte[] byteArray = Encoding.UTF8.GetBytes(reqContent);
                // Set the ContentType property of the WebRequest.
                request.ContentType = "application/x-www-form-urlencoded";
                // Set the ContentLength property of the WebRequest.
                request.ContentLength = byteArray.Length;
                // Get the request stream.
                Stream dataStream = request.GetRequestStream();
                // Write the data to the request stream.
                dataStream.Write(byteArray, 0, byteArray.Length);
                // Close the Stream object.
                dataStream.Close();

                WebResponse response = request.GetResponse();
                //Console.WriteLine(response.GetResponseStream().ToString());
                dataStream = response.GetResponseStream();


                keywords = ExtractFromAlchemyKeywordXML(dataStream);
                string line = "";
                foreach (string keyword in keywords)
                {
                    line += keyword + ",";
                }
                line = line.Substring(0, line.Length - 1);

                keywordsFile.AppendLine(line);

                readLine = textFile.ReadLine();
            }

            System.IO.File.WriteAllText("D:\\alchemyKeywords.txt", keywordsFile.ToString());
        }

        public static ArrayList ExtractFromAlchemyKeywordXML(Stream xmlStream)
        {
            XmlReader r = XmlReader.Create(xmlStream);
            XmlSpace sp = new XmlSpace();

            XPathDocument doc = new XPathDocument(r);
            XPathNavigator nav = doc.CreateNavigator();

            //XmlNamespaceManager manager = new XmlNamespaceManager(nav.NameTable);
            //manager.AddNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#");
            //manager.AddNamespace("aapi", "http://rdf.alchemyapi.com/rdf/v1/s/aapi-schema#");
            //manager.AddNamespace("owl", "http://www.w3.org/2002/07/owl#");
            //manager.AddNamespace("geo", "http://www.w3.org/2003/01/geo/wgs84_pos#");
            //manager.AddNamespace("base", "http://rdf.alchemyapi.com/rdf/v1/r/response.rdf");

            //XPathNodeIterator iter = nav.Select("//rdf:Description[contains(@rdf:ID,'-gk_')]/aapi:Name", manager);
            XPathNodeIterator iter = nav.Select("//keyword/text");

            ArrayList keywords = new ArrayList();
            while (iter.MoveNext())
                keywords.Add(iter.Current.Value);

            return keywords;
        }
    }
}
