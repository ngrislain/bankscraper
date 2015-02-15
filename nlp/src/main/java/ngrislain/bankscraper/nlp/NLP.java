package ngrislain.bankscraper.nlp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;

import com.google.common.base.Function;
import com.google.common.collect.HashMultiset;
import com.google.common.collect.Multiset;
import com.google.common.collect.Multisets;

public class NLP {
	public static final int NUM_OF_SYMBOLS = 5000;
	public static final int NUM_OF_FEATURES = 100000;
	public static int[] SYMBOL_FEATURES;
	public static final String CORPUS_PATH = "/Users/nicolas/Data/nlp";
	public static final String WORD_RE = "[0123456789"
			+ "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
			+ "abcdefghijklmnopqrstuvwxyz"
			+ "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß"
			+ "àáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ]+";
	public static final String LINK_RE = "[\\-´'`]";
	public static final String PAUSE_RE = "[,;:()]";
	public static final String STOP_RE = "[.?!]";
	public static final Pattern ELEMENT_PAT = Pattern.compile(String.format("(%s)|(%s)|(%s)|(%s)", WORD_RE, LINK_RE, PAUSE_RE, STOP_RE));
	
	/*
	 * Record words and export to csv
	 */
	public static HashMultiset<String> symbolCounts = HashMultiset.create();
	public static HashMultiset<String> topSymbolCounts = HashMultiset.create();
	public static long counts = 0;
	/** Count symbols */
	public static Function<String, Void> countSymbols = new Function<String, Void>() {
		public Void apply(String symbol) {
			counts++;
			if (counts%10000000 == 0) {
				System.out.println(counts);
				System.out.println(symbolCounts.entrySet().size());
			}
			symbolCounts.add(symbol);
			return null;
		}
	};
	/** Count top symbols and clear the main table */
	public static void topSymbolCount() {
		topSymbolCounts.clear();
		int count = 0;
		for (Multiset.Entry<String> entry : Multisets.copyHighestCountFirst(symbolCounts).entrySet()) {
			topSymbolCounts.add(entry.getElement(), entry.getCount());
			if (++count>NUM_OF_SYMBOLS) break;
		}
		symbolCounts.clear();
	}
	/** Export to csv */
	public static void exportTopSymbolCount(String path) {
		try {
			BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(path));
			for (Multiset.Entry<String> entry : Multisets.copyHighestCountFirst(topSymbolCounts).entrySet()) {
				bufferedWriter.write(String.format("%s, %d\n", entry.getElement(), entry.getCount()));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/*
	 * Process significant symbols
	 */
	/** Process significant symbols */
	public static Function<String, Void> processSymbols = new Function<String, Void>() {
		public Void apply(String symbol) {
			if (topSymbolCounts.contains(symbol)) {
				System.out.print(symbol);
				System.out.print(" ");
				if ("<STOP>".equals(symbol)) System.out.println();
			} else {
				System.out.print(". ");
			}
			return null;
		}
	};
	
	/*
	 * Split and match symbols 
	 */
	/** Matches a symbol */
	public static String matchSymbol(Matcher wordMatcher) {
		if (wordMatcher.group(1) != null) {
			return wordMatcher.group(1).toLowerCase();
		} else if (wordMatcher.group(2) != null) {
			return "<LINK>";
		} else if (wordMatcher.group(3) != null) {
			return "<PAUSE>";
		} else if (wordMatcher.group(4) != null) {
			return "<STOP>";
		} else {
			return "<OTHER>";
		}
	}
	
	/** Split to symbols then process them */
	public static void splitProcess(String filePath, Function<String, Void> process) {
		try {
			BufferedReader reader = new BufferedReader(new FileReader(CORPUS_PATH+"/"+filePath));
			// We count the words
			long count = 0;
			while (reader.ready()) {
				Matcher wordMatcher = ELEMENT_PAT.matcher(reader.readLine());
				while (wordMatcher.find()) {
					count++;
					process.apply(matchSymbol(wordMatcher));
				}
				if (count>10000000) break;
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Throwable e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
//		split("frwikisource-20141228-pages-meta-current.xml");
		splitProcess("frwiki-20150119-pages-meta-current1.xml", countSymbols);
		topSymbolCount();
		exportTopSymbolCount("/Users/nicolas/Desktop/test.csv");
		
		
		SYMBOL_FEATURES = new int[NUM_OF_SYMBOLS*NUM_OF_FEATURES];
		splitProcess("frwiki-20150119-pages-meta-current1.xml", processSymbols);
		
	}
}
