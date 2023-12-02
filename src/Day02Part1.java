import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Locale;
import java.util.Optional;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Day02Part1 {
    private String fileName = this.getClass().getName();
    private final int RED = 12;
    private final int GREEN = 13;
    private final int BLUE = 14;

    private int matchNumber(String regex, String line, boolean prefix) {
        Pattern pattern = Pattern.compile(prefix ? regex + " (\\d+)" : "(\\d+) " + regex);
        Matcher matcher = pattern.matcher(line);
        if (matcher.find()) {
            return Integer.parseInt(matcher.group(1));
        } else {
            return 0;
        }
    }

    private boolean isDrawPossible(String draw) {
        int red = matchNumber("red", draw,false);
        int blue = matchNumber("blue", draw,false);
        int green = matchNumber("green", draw,false);
        return (red <= RED) && (blue <= BLUE) && (green <= GREEN);
    }

    private void solve() throws IOException {

        Stream<String> lines = br.lines();
        Optional<Integer> answer = lines.map((l) -> {
            int gameNumber = matchNumber("Game", l, true);
            String[] draws = l.split(";");
            Optional<Boolean> gamePossible = Arrays.stream(draws).
                    map(this::isDrawPossible).
                    reduce((game1, game2) -> game1 && game2);
            return gamePossible.isPresent() && gamePossible.get() ? gameNumber : 0;
        }).reduce(Integer::sum);
        answer.ifPresent(out::println);
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
    private StringTokenizer in;
    private PrintWriter out;

    private String nextToken() throws IOException {
        while (in == null || !in.hasMoreTokens()) {
            in = new StringTokenizer(br.readLine());
        }
        return in.nextToken();
    }

    private int nextInt() throws IOException {
        return Integer.parseInt(nextToken());
    }

    private double nextDouble() throws IOException {
        return Double.parseDouble(nextToken());
    }

    private long nextLong() throws IOException {
        return Long.parseLong(nextToken());
    }

    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);
        new Day02Part1().run();
    }
}