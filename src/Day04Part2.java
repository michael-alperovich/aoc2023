import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Day04Part2 {
    private String fileName = this.getClass().getName();

    private void solve() throws IOException {
        Stream<String> lines = br.lines();
        List<Integer> matchingCount = lines.map((l) -> {
            String[] numberGroups = l.split(":")[1].split("\\|");
            HashSet<String> winning = new HashSet<>(Arrays.asList(numberGroups[0].split(" ")));
            HashSet<String> ours = new HashSet<>(Arrays.asList(numberGroups[1].split(" ")));
            ours.retainAll(winning);
            ours.remove("");
            return ours.size();
        }).collect(Collectors.toList());
        ArrayList<Integer> cardCnt = new ArrayList<>(Collections.nCopies(matchingCount.size(), 1));
        int answer = 0;
        for (int i = 0; i < cardCnt.size(); i++) {
            answer += cardCnt.get(i);
            for (int j = i + 1; j < Integer.min(cardCnt.size(), i + matchingCount.get(i) + 1); j++) {
                cardCnt.set(j, cardCnt.get(j) + cardCnt.get(i));
            }
        }
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
        new Day04Part2().run();
    }
}