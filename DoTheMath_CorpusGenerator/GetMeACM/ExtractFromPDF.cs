using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.XPath;
using System.Collections;
using System.Net;
using System.IO;


namespace GetMeACM
{
    class ExtractFromPaper
    {
        public ArrayList ExtractCCS(string paperPath)
        {
            ArrayList ccsClasses = new ArrayList();
            StreamReader paper = new StreamReader(paperPath);
            string paperLine = paper.ReadLine();
            while (!paperLine.StartsWith("Categories and Subject Descriptors:", StringComparison.CurrentCultureIgnoreCase) &&
                !paperLine.StartsWith("Categories  and  Subject  Descriptors:", StringComparison.CurrentCultureIgnoreCase))
                paperLine = paper.ReadLine();
            
            string ccsLine = "";
            while (!paperLine.StartsWith("General Terms:", StringComparison.CurrentCultureIgnoreCase)
                && !paperLine.StartsWith("Additional Key Words and Phrases:", StringComparison.CurrentCultureIgnoreCase))
            {
                ccsLine += paperLine;
                paperLine = paper.ReadLine();
            }

            string[] words = ccsLine.Split(' ',';','[',']');
            foreach (string word in words)
            {
                if (System.Text.RegularExpressions.Regex.IsMatch(word, "[A-Z]{1}[.]{1}[0-9m]+([.]{1}[0-9]+)?", System.Text.RegularExpressions.RegexOptions.IgnoreCase))
                {
                    //Console.WriteLine(word);
                    ccsClasses.Add(word);
                }
            }

            return ccsClasses;
        }
    }
}
