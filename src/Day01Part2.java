import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.Locale;
import java.util.StringTokenizer;

public class Day01Part2 {
    private String fileName = this.getClass().getName();

    private void solve() throws IOException {
        int sum = 0;
        String line;
        String[] spelledDigits = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
        while ((line = br.readLine()) != null) {
            int first = 0;
            int last = 0;
            for (int i = 0; i < line.length(); i++) {
                char c = line.charAt(i);
                if (Character.isDigit(c)) {
                    if (first == 0) {
                        first = c - '0';
                    }
                    last = c - '0';
                } else {
                    boolean[] tracking = new boolean[spelledDigits.length];
                    Arrays.fill(tracking, true);
                    boolean stop = false;
                    int j = i;
                    while (!stop && j < line.length()) {
                        boolean continueChecking = false;
                        for (int t = 0; t < tracking.length; t++) {
                            if (tracking[t]) {
                                String digit = spelledDigits[t];
                                if (digit.charAt(j - i) == line.charAt(j)) {
                                    continueChecking = true;
                                    if (digit.length() == j - i + 1) {
                                        if (first == 0) {
                                            first = t;
                                        }
                                        last = t;
                                        continueChecking = false;
                                        break;
                                    }
                                } else {
                                    tracking[t] = false;
                                }
                            }
                        }
                        stop = !continueChecking;
                        j++;
                    }
                }
            }
            int number = first * 10 + last;
            sum += number;
        }
        out.println(sum);
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
        new Day01Part2().run();
    }
}