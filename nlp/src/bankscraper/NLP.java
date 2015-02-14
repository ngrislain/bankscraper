package bankscraper;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;

public class NLP {
	public static final String CORPUS_PATH = "/Users/nicolas/Data/nlp";
	public static final String WORD_RE = "[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàéèêïœç\\-]+";
	public static final String PAUSE_RE = "[,;:]";
	public static final String STOP_RE = "[.?!]";
	public static final Pattern ELEMENT_PAT = Pattern.compile(String.format("(%s)|(%s)|(%s)", WORD_RE, PAUSE_RE, STOP_RE));
	
	public static void process(String word) {
		System.out.println(word);
	}
	
	public static void split(String filePath, MethodHandle handle) {
		try {
			BufferedReader reader = new BufferedReader(new FileReader(CORPUS_PATH+"/"+filePath));
			handle.invokeExact(reader.readLine());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Throwable e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		split("frwikisource-20141228-pages-meta-current.xml", MethodHandles.invoker(MethodType.methodType(void.class, String.class)));
	}
}
