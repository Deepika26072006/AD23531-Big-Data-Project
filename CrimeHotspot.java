import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.lang.Math;

public class CrimeHotspot {

    public static class CrimeMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text outKey = new Text();
        private static final double GRID_SIZE = 0.01; // degrees ~1km (tweak as needed)

        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            if (line == null || line.length() == 0) return;
            if (line.startsWith("event_id")) return; // header

            String[] parts = line.split(",", -1);
            if (parts.length < 6) return;

            try {
                String eventTime = parts[1].trim(); // yyyy-mm-dd HH:MM:SS (or iso)
                String date = eventTime.split(" ")[0];
                String city = parts[2].trim();
                double lat = Double.parseDouble(parts[4].trim());
                double lon = Double.parseDouble(parts[5].trim());

                int gx = (int)Math.floor(lat / GRID_SIZE);
                int gy = (int)Math.floor(lon / GRID_SIZE);

                // key format: city|gx|gy|date
                String keyOut = city + "|" + gx + "|" + gy + "|" + date;
                outKey.set(keyOut);
                context.write(outKey, one);
            } catch (Exception e) {
                // ignore malformed line
            }
        }
    }

    public static class CrimeReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable v : values) sum += v.get();
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: CrimeHotspot <input path> <output path>");
            System.exit(-1);
        }
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Crime Hotspot Grid Count");
        job.setJarByClass(CrimeHotspot.class);
        job.setMapperClass(CrimeMapper.class);
        job.setCombinerClass(CrimeReducer.class);
        job.setReducerClass(CrimeReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
