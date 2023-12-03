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

public class Day02Part2 {
    private String fileName = this.getClass().getName();

    class Draw {
        public int red;
        public int green;
        public int blue;
    }
    private int matchNumber(String regex, String line, boolean prefix) {
        Pattern pattern = Pattern.compile(prefix ? regex + " (\\d+)" : "(\\d+) " + regex);
        Matcher matcher = pattern.matcher(line);
        if (matcher.find()) {
            return Integer.parseInt(matcher.group(1));
        } else {
            return 0;
        }
    }

    private Draw parseDraw(String drawString) {
        Draw draw = new Draw();
        draw.red = matchNumber("red", drawString,false);
        draw.blue = matchNumber("blue", drawString,false);
        draw.green = matchNumber("green", drawString,false);
        return draw;
    }

    private Draw combineDraws(Draw draw1, Draw draw2) {
        Draw combinedDraw = new Draw();
        combinedDraw.red = Integer.max(draw1.red, draw2.red);
        combinedDraw.blue = Integer.max(draw1.blue, draw2.blue);
        combinedDraw.green = Integer.max(draw1.green, draw2.green);
        return combinedDraw;
    }

    private void solve() throws IOException {
        Stream<String> lines = br.lines();
        Optional<Integer> answer = lines.map((l) -> {
            String[] draws = l.split(";");
            Optional<Draw> minimumCubesOpt = Arrays.stream(draws).
                    map(this::parseDraw).
                    reduce(this::combineDraws);
            Draw minimumCubes = minimumCubesOpt.get();
            return minimumCubes.red * minimumCubes.blue * minimumCubes.green;
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
        new Day02Part2().run();
    }
}