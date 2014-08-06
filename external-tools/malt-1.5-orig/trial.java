
import java.io.*;

import org.maltparser.core.exception.*;
import org.maltparser.*;
import org.maltparser.core.syntaxgraph.DependencyStructure;


public class maltParserWrap {

	public static void main(String[] args) {
		try {
			MaltParserService service = new MaltParserService();
			service.initializeParserModel("-c farsiMALTModel -m parse");
			BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		    	String[] tokens = new String[100];
		    	while (true){
		    		int i = 0;
		    		try {
					while ((tokens[i] = in.readLine()) != null && tokens[i].length() != 0){
						i++;
					}
			
				} catch (IOException e) {
					e.printStackTrace();
				}
				System.out.println(tokens[0]);		    
			    	DependencyStructure graph = service.parse(tokens);
			    	System.out.println(graph);
		    	}
		        //service.terminateParserModel();
		}
		catch (MaltChainedException e) {
			System.err.println("MaltParser exception: " + e.getMessage());
			
		}

	}

}
