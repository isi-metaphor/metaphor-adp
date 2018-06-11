import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

import org.maltparser.MaltParserService;
import org.maltparser.core.symbol.SymbolTable;
import org.maltparser.core.syntaxgraph.DependencyStructure;
import org.maltparser.core.syntaxgraph.edge.Edge;
import org.maltparser.core.syntaxgraph.node.DependencyNode;

public class MaltParserWrap {

    public static void main(String[] args) {
        try {
            String argsLine = null;
            for (String a: args) {
                a = a.trim();
                if (a != null && !a.isEmpty()) {
                    if (argsLine == null)
                        argsLine = a;
                    else argsLine += " " + a;
                }
            }
            MaltParserService service = new MaltParserService();
            service.initializeParserModel(argsLine);
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));

            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(System.out, "UTF-8"));
            while (true) {
                String line = null;
                ArrayList<String> lines = new ArrayList<String>();
                while ((line = reader.readLine()) != null) {
                    if (!line.equals("END")) {

                        if (line.trim().length() == 0) {
                            DependencyStructure graph = service.parse(lines.toArray(new String[lines.size()]));

                            for (int i = 1; i <= graph.getHighestDependencyNodeIndex(); i++) {

                                DependencyNode node = graph.getDependencyNode(i);
                                if (node != null) {
                                    for (SymbolTable table : node.getLabelTypes()) {
                                        writer.write(node.getLabelSymbol(table) + "\t");
                                    }
                                    if (node.hasHead()) {
                                        Edge e = node.getHeadEdge();
                                        writer.write(e.getSource().getIndex() + "\t");
                                        if (e.isLabeled()) {
                                            for (SymbolTable table : e.getLabelTypes()) {
                                                writer.write(e.getLabelSymbol(table) + "\t");
                                            }
                                        } else {
                                            for (SymbolTable table : graph.getDefaultRootEdgeLabels().keySet()) {
                                                writer.write(graph.getDefaultRootEdgeLabelSymbol(table) + "\t");
                                            }
                                        }
                                    }
                                    writer.write("_\t_\n");
                                    writer.flush();
                                }
                            }
                            writer.write('\n');
                            writer.flush();
                            lines.clear();

                        } else {
                            lines.add(line);
                        }
                    } else {
                        writer.write("END");
                        writer.flush();
                        System.exit(0);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace(System.err);
        }
    }
}
