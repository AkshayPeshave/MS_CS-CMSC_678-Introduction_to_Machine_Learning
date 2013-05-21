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
using System.Collections;
using MySql.Data;
using MySql.Data.MySqlClient;


namespace GetMeACM
{
    class CreateLearningDataSet
    {
        public void ExtractUserKeywords()
        {
            StreamReader csv = 
                new StreamReader("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\ACM_meta.csv");

            //StreamWriter asach = new StreamWriter("D:\\againGhe.txt");

            string line = csv.ReadLine();
            StringBuilder sb = new StringBuilder();

            while (line != null)
            {
                string keywordField = line.Split('\t')[4];
                string[] keywords = keywordField.Substring(1, keywordField.Length - 2).Split(';');

                string mergedKeywords="";
                foreach (string s in keywords)
                {
                    mergedKeywords += s + " ";
                }
                sb.AppendLine(mergedKeywords);

                line = csv.ReadLine();
            }

            System.IO.File.WriteAllText("D:\\ghe.txt", sb.ToString());
            //asach.Write(sb.ToString());
            csv.Close();
        }

        public void ExtractUserKeyPhrases()
        {
            StreamReader csv =
                new StreamReader("D:\\Workspace\\CMSC 678 - Machine Learning\\Project\\PaperDump\\ACM_meta.csv");

            //StreamWriter asach = new StreamWriter("D:\\againGhe.txt");

            string line = csv.ReadLine();
            StringBuilder sb = new StringBuilder();

            while (line != null)
            {
                string keywordField = line.Split('\t')[4];

                sb.AppendLine(keywordField.Substring(1, keywordField.Length - 2));

                line = csv.ReadLine();
            }

            System.IO.File.WriteAllText("D:\\userKeyPhrases.txt", sb.ToString());
            //asach.Write(sb.ToString());
            csv.Close();
        }

        public void ExctractMSCTopics()
        {
            string connStr = "server=localhost;user=root;database=csv_db;port=3306;";
            MySqlConnection conn = new MySqlConnection(connStr);
            try
            {
                Console.WriteLine("Connecting to MySQL...");
                conn.Open();

                StreamReader userKeywordsFile = new StreamReader(@"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\UserKeywords.txt");
                StringBuilder sb = new StringBuilder();

                
                string userKeywords = userKeywordsFile.ReadLine();
                int recordNum = 0;
                string query = "";
                while (userKeywords != null)
                {
                    recordNum++;
                    query = "SELECT `UID` FROM `table 3` " +
                            "WHERE MATCH(`msc_topic`) AGAINST ('" + userKeywords + "') "+
                            "LIMIT 5";
                    MySqlCommand cmd = new MySqlCommand(query, conn);

                    MySqlDataReader reader = cmd.ExecuteReader();

                    while (reader.Read())
                    {
                        sb.AppendLine(recordNum + " " + reader[0]);
                    }

                    reader.Close();
                    userKeywords = userKeywordsFile.ReadLine();
                }
                userKeywordsFile.Close();
                System.IO.File.WriteAllText(@"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\MSCClassification.txt", sb.ToString());
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
            
            conn.Close();
            Console.WriteLine("Done.");
        }

        public void ExtractCCSClassification()
        {
            ExtractFromPaper ext = new ExtractFromPaper();

            StreamReader papers = new StreamReader("ACM Papers.txt");
            StringBuilder sb = new StringBuilder();

            string paper = papers.ReadLine();

            ArrayList ccs = new ArrayList();
            int index = 0;

            while (paper != null)
            {
                index++;
                ccs = ext.ExtractCCS
                    (@"D:\Workspace\CMSC 678 - Machine Learning\Project\PaperDump\TEXT\" + paper + ".txt");
                string ccsLine = "";
                foreach (Object obj in ccs)
                {
                    sb.AppendLine(index + " " + (string)obj);
                }
                
                paper = papers.ReadLine();
            }

            System.IO.File.WriteAllText("D:\\CCSLearningSet.txt", sb.ToString());
        }
    }
}
