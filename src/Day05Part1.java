import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import java.util.stream.Collectors;

public class Day05Part1 {
    private String fileName = this.getClass().getName();
    private List<Long> seeds = new ArrayList<>();
    private ArrayList<ArrayList<AlmanacRange>> maps = new ArrayList<>();

    class AlmanacRange {
        long range, sourceStart, sourceEnd, destinationStart, destinationEnd;

        public AlmanacRange(String destinationStart, String sourceStart, String range) {
            this.range = Long.parseLong(range);
            this.sourceStart = Long.parseLong(sourceStart);
            this.destinationStart = Long.parseLong(destinationStart);
            this.sourceEnd = Long.parseLong(sourceStart) + this.range;
            this.destinationEnd = Long.parseLong(destinationStart) + this.range;
        }

        public boolean contains(long n) {
            return (this.sourceStart <= n) && (n < this.sourceEnd);
        }

        public long getDestination(long n) {
            return n + this.destinationStart - this.sourceStart;
        }
    }

    private void read() throws IOException {
        seeds = Arrays.stream(br.readLine().split("seeds: ")[1].split(" "))
                .map(Long::parseLong)
                .collect(Collectors.toList());
        String line;
        boolean skip = false;
        while ((line = br.readLine()) != null) {
            if (skip) {
                skip = false;
            } else if (line.equals("")) {
                maps.add(new ArrayList<>());
                skip = true;
            } else {
                String[] rangeString = line.split(" ");
                AlmanacRange range = new AlmanacRange(rangeString[0], rangeString[1], rangeString[2]);
                maps.get(maps.size() - 1).add(range);
            }
        }
    }

    private void solve() throws IOException {
        read();
        long lowestLocation = seeds.stream().map((s) -> {
            long location = s;
            for (ArrayList<AlmanacRange> m: maps) {
                long currentPosition = location;
                location = m.stream().filter((r) -> r.contains(currentPosition))
                        .map((r) -> r.getDestination(currentPosition))
                        .findFirst()
                        .orElse(currentPosition);
            }
            return location;
        }).reduce(Long::min).orElse(0L);
        out.println(lowestLocation);
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
        new Day05Part1().run();
    }
}