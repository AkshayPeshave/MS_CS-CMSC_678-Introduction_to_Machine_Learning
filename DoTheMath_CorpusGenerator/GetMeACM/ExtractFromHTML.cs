using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.XPath;
using System.Collections;
using System.Net;
using System.IO;
using HtmlAgilityPack;
using System.Xml;

namespace GetMeACM
{
    class ExtractFromHTML
    {
        private string [] papers;

        public ExtractFromHTML(string dumpPath)
        {
            papers = Directory.GetFiles( dumpPath, "*.htm", SearchOption.TopDirectoryOnly);
            //foreach (string paper in papers)
            //{
            //    Console.WriteLine(paper);
            //}
        }

        public void ExtractMetadata()
        {
            HtmlWeb web = new HtmlWeb();
            FileStream csv = new FileStream("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\ACM_meta.csv", FileMode.Create);
            foreach(string paper in papers)
            {
                HtmlDocument doc = web.Load(paper);
                HtmlNodeCollection nodes;
                string line = "";

                nodes = doc.DocumentNode.SelectNodes("//a[contains(@href,'http://dx.doi.org/')]");
                line += "{" + nodes[0].InnerText + "}\t";
                line += "{" + nodes[0].GetAttributeValue("href", "not found") + "}\t";

                
                
                nodes = doc.DocumentNode.SelectNodes("//div[@id='divmain']/div/h1/strong");

                Console.WriteLine(nodes[0].InnerHtml);
                line += "{"+nodes[0].InnerHtml+"}\t";

                //Console.WriteLine(nodes[0].SelectSingleNode("//a[@name='FullTextPdf' or @name='FullTextPDF']").GetAttributeValue("href", "notfound"));
                //line += "{" + nodes[0].SelectSingleNode("//a[@name='FullTextPdf' or @name='FullTextPDF']").GetAttributeValue("href", "notfound")  + "}\t";

                //Console.WriteLine();
                line += "{";
                nodes = doc.DocumentNode.SelectNodes("//div[@id='divmain']/table/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/a");
                if (nodes == null)
                    nodes = doc.DocumentNode.SelectNodes("//div[@id='divmain']/table/tr/td[1]/table[2]/tr/td[2]/a");

                foreach (HtmlNode author in nodes)
                {
                    Console.WriteLine(author.InnerText);
                    line += author.InnerText + ";";
                }
                line = line.Substring(0, line.Length - 1) + "}\t";

                line += "{";
                nodes = doc.DocumentNode.SelectNodes("//a[contains(@href,'results.cfm?')]");
                foreach (HtmlNode node in nodes)
                {
                    Console.Write(node.InnerText + ",");
                    line += node.InnerText + ";";

                }
                line = line.Substring(0, line.Length - 1) + "}\n";
                Console.WriteLine("\n");

                //nodes = doc.DocumentNode.SelectNodes("//div[@id='abstract']/div/div/p");
                //foreach (HtmlNode para in nodes)
                //{
                //    Console.Write(para.InnerText);
                //}

                

                //write to csv
                byte[] lineBytes = Encoding.UTF8.GetBytes(line);
                csv.Write(lineBytes, 0, lineBytes.Length);

                
            }
            csv.Close();
        }
    }
}
