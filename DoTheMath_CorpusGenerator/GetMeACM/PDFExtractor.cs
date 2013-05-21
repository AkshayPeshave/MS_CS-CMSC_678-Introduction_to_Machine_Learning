using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using com.snowtide.pdf;
using java.lang;

namespace GetMeACM
{
    class PDFExtractor
    {
        public void ExtractPDFContent(string path,string destination)
        {
            string pdfFilePath = path;
            java.io.BufferedWriter writer = new java.io.BufferedWriter(new java.io.OutputStreamWriter
                (new java.io.FileOutputStream(destination)));
            // get OutputTarget configured to pipe text to the provided file path
            OutputTarget tgt = new OutputTarget(writer);
            using (PDFTextStream pdfts = new PDFTextStream(pdfFilePath))
            {
                pdfts.pipe(tgt);
            }
            System.Console.WriteLine("The text extracted from {0} is:",
                pdfFilePath);
            //System.Console.WriteLine(tgt.);
        }
    }
}
