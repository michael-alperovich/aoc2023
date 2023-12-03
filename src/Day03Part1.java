import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import java.util.stream.Stream;

public class Day03Part1 {
    private String fileName = this.getClass().getName();
    private ArrayList<ArrayList<SchematicElement>> schematic = new ArrayList<>();

    class SchematicElement {
        int i, j;
        char c;

        public SchematicElement(int i, int j, char c) {
            this.i = i;
            this.j = j;
            this.c = c;
        }

        public boolean isNumber() {
            boolean isDigit = Character.isDigit(this.c);
            boolean hasLeftNeighbor = this.j > 0;
            boolean isLeftNeighborDigit = hasLeftNeighbor && Character.isDigit(schematic.get(this.i).get(this.j - 1).c);
            return isDigit && !isLeftNeighborDigit;
        }

        public PotentialPartNumber getNumber() {
            int value = 0;
            int maxRight = this.j;
            SchematicElement e = this;
            while (Character.isDigit(e.c)) {
                value = value * 10 + (e.c - '0');
                maxRight = e.j;
                if (e.j + 1 >= schematic.get(0).size()) {
                    break;
                } else {
                    e = schematic.get(e.i).get(e.j + 1);
                }
            }
            return new PotentialPartNumber(value, this.i, this.j, maxRight);
        }
    }

    class PotentialPartNumber {
        int value, i, leftJ, rightJ;

        public PotentialPartNumber(int value, int i, int leftJ, int rightJ) {
            this.value = value;
            this.i = i;
            this.leftJ = leftJ;
            this.rightJ = rightJ;
        }

        public boolean isPartNumber() {
            boolean check = false;
            for (int iCheck = this.i - 1; iCheck <= this.i + 1; iCheck++) {
                for (int jCheck = this.leftJ - 1; jCheck <= this.rightJ +1; jCheck++) {
                    if ((0 <= iCheck && iCheck < schematic.size()) && (0 <= jCheck && jCheck < schematic.get(0).size())) {
                        SchematicElement e = schematic.get(iCheck).get(jCheck);
                        if (!Character.isDigit(e.c) && e.c != '.') {
                            check = true;
                        }
                    }
                }
            }
            return check;
        }

        public int getValue() {
            return this.value;
        }
    }

    private void solve() throws IOException {
        Stream<String> lines = br.lines();

        lines.forEachOrdered((l) -> {
            ArrayList<SchematicElement> row = new ArrayList<>();
            for (char c : l.toCharArray()) {
                row.add(new SchematicElement(schematic.size(), row.size(), c));
            }
            schematic.add(row);
        });

        int answer = schematic.stream().flatMap(Collection::stream)
                .filter(SchematicElement::isNumber)
                .map(SchematicElement::getNumber)
                .filter(PotentialPartNumber::isPartNumber)
                .mapToInt(PotentialPartNumber::getValue)
                .sum();
        out.println(answer);
    }

    private void run() {
        try {
            br = new BufferedReader(new FileReader("resources/" + fileName + "_in.txt"));
            out = new PrintWriter("resources/" + fileName + "_out.txt");
            solve();
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }


    private BufferedReader br;
    private PrintWriter out;

    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        new Day03Part1().run();
    }
}