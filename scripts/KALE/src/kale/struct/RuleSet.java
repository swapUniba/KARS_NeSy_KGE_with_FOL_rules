package kale.struct;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.TreeMap;

import basic.util.StringSplitter;
import kale.struct.Triple;

public class RuleSet {
	private int iNumberOfEntities;
	private int iNumberOfRelations;
	private int iNumberOfRules;
	public ArrayList<Rule> pRule = null;
	
	public RuleSet() {
	}
	
	public RuleSet(int iEntities, int iRelations) throws Exception {
		iNumberOfEntities = iEntities;
		iNumberOfRelations = iRelations;
	}
	
	public int entities() {
		return iNumberOfEntities;
	}
	
	public int relations() {
		return iNumberOfRelations;
	}
	
	public int rules() {
		return iNumberOfRules;
	}
	
	public String ruledimensions() {
		String str = "";
		int c2 = 0, c3=0, c4=0;
		for (Rule rule : pRule) {
			if (rule.fouTriple() == null && rule.trdTriple() == null) {
				c2++;
			} else if (rule.trdTriple() == null) {
				c3++;
			} else {
				c4++;
			}
			
		}
		
		str = "2=: " + c2 + "; 3=" + c3 + "; 4=" + c4;
		return str;
	}
	
	public Rule get(int iID) throws Exception {
		if (iID < 0 || iID >= iNumberOfRules) {
			throw new Exception("getRule error in RuleSet: ID out of range");
		}
		return pRule.get(iID);
	}
	
	public void load(String fnInput) throws Exception {
		BufferedReader reader = new BufferedReader(new InputStreamReader(
				new FileInputStream(fnInput), "UTF-8"));
		pRule = new ArrayList<Rule>();
		
		String line = "";
		while ((line = reader.readLine()) != null) {
			String[] tokens = StringSplitter.RemoveEmptyEntries(StringSplitter
					.split("\t() ", line));
			
			
			/*if (tokens.length != 6 && tokens.length != 9 && tokens.length != 12) {
				throw new Exception("load error in RuleSet: data format incorrect");
			}*/

			int iFstHead = Integer.parseInt(tokens[0]);
			int iFstTail = Integer.parseInt(tokens[2]);
			int iFstRelation = Integer.parseInt(tokens[1]);
//			System.out.println(iFstHead+" "+iFstTail+" "+iFstRelation);
			if (iFstHead < 0 || iFstHead >= iNumberOfEntities) {
				throw new Exception("load error in RuleSet: 1st head entity ID out of range");
			}
			if (iFstTail < 0 || iFstTail >= iNumberOfEntities) {
				throw new Exception("load error in RuleSet: 1st tail entity ID out of range");
			}
			System.out.println(iFstRelation);
			if (iFstRelation < 0 || iFstRelation >= iNumberOfRelations) {
				throw new Exception("load error in RuleSet: 1st relation ID out of range");
			}
			Triple fstTriple = new Triple(iFstHead, iFstTail, iFstRelation);
			
			int iSndHead = Integer.parseInt(tokens[3]);
			int iSndTail = Integer.parseInt(tokens[5]);
			int iSndRelation = Integer.parseInt(tokens[4]);
			if (iSndHead < 0 || iSndHead >= iNumberOfEntities) {
				throw new Exception("load error in RuleSet: 2nd head entity ID out of range");
			}
			if (iSndTail < 0 || iSndTail >= iNumberOfEntities) {
				throw new Exception("load error in RuleSet: 2nd tail entity ID out of range");
			}
			if (iSndRelation < 0 || iSndRelation >= iNumberOfRelations) {
				throw new Exception("load error in RuleSet: 2nd relation ID out of range");
			}
			Triple sndTriple = new Triple(iSndHead, iSndTail, iSndRelation);
			
			if (tokens.length == 6){
				pRule.add(new Rule(fstTriple, sndTriple));
			}
			else if (tokens.length == 9) {
				
				int iTrdHead = Integer.parseInt(tokens[6]);
				int iTrdTail = Integer.parseInt(tokens[8]);
				int iTrdRelation = Integer.parseInt(tokens[7]);
//				System.out.println(iTrdHead+" "+iTrdTail+" "+iTrdRelation);
				
				if (iTrdHead < 0 || iTrdHead >= iNumberOfEntities) {
					throw new Exception("load error in RuleSet: 3rd head entity ID out of range");
				}
				if (iTrdTail < 0 || iTrdTail >= iNumberOfEntities) {
					throw new Exception("load error in RuleSet: 3rd tail entity ID out of range");
				}
				if (iTrdRelation < 0 || iTrdRelation >= iNumberOfRelations) {
					throw new Exception("load error in RuleSet: 3rd relation ID out of range");
				}
				Triple trdTriple = new Triple(iTrdHead, iTrdTail, iTrdRelation);
				
				pRule.add(new Rule(fstTriple, sndTriple, trdTriple));
				
			} else {
				
				int iTrdHead = Integer.parseInt(tokens[6]);
				int iTrdTail = Integer.parseInt(tokens[8]);
				int iTrdRelation = Integer.parseInt(tokens[7]);
				
				if (iTrdHead < 0 || iTrdHead >= iNumberOfEntities) {
					throw new Exception("load error in RuleSet: 3rd head entity ID out of range");
				}
				if (iTrdTail < 0 || iTrdTail >= iNumberOfEntities) {
					throw new Exception("load error in RuleSet: 3rd tail entity ID out of range");
				}
				if (iTrdRelation < 0 || iTrdRelation >= iNumberOfRelations) {
					throw new Exception("load error in RuleSet: 3rd relation ID out of range");
				}
				Triple trdTriple = new Triple(iTrdHead, iTrdTail, iTrdRelation);
				
				int iFouHead = Integer.parseInt(tokens[9]);
				int iFouTail = Integer.parseInt(tokens[11]);
				int iFouRelation = Integer.parseInt(tokens[10]);
//				System.out.println(iTrdHead+" "+iTrdTail+" "+iTrdRelation);
				
				if (iFouHead < 0 || iFouHead >= iNumberOfEntities) {
					throw new Exception("load error in RuleSet: 4rd head entity ID out of range");
				}
				if (iFouTail < 0 || iFouTail >= iNumberOfEntities) {
					throw new Exception("load error in RuleSet: 4rd tail entity ID out of range");
				}
				if (iFouRelation < 0 || iFouRelation >= iNumberOfRelations) {
					throw new Exception("load error in RuleSet: 4rd relation ID out of range");
				}
				Triple fouTriple = new Triple(iFouHead, iFouTail, iFouRelation);
				
				pRule.add(new Rule(fstTriple, sndTriple, trdTriple, fouTriple));
			}
		}
		
		System.out.println(ruledimensions());
		
		iNumberOfRules = pRule.size();
		System.out.println("Dimension of rule set: " + iNumberOfRules);
		reader.close();
	}
	
	public void randomShuffle() {
		TreeMap<Double, Rule> tmpMap = new TreeMap<Double, Rule>();
		
		for (int iID = 0; iID < iNumberOfRules; iID++) {
			int m = pRule.get(iID).fstTriple().head();
			int n = pRule.get(iID).fstTriple().tail();
			int s = pRule.get(iID).fstTriple().relation();
			Triple fstTriple = new Triple(m, n, s);
			int p = pRule.get(iID).sndTriple().head();
			int q = pRule.get(iID).sndTriple().tail();
			int t = pRule.get(iID).sndTriple().relation();
			Triple sndTriple = new Triple(p, q, t);
			if(pRule.get(iID).trdTriple()==null && pRule.get(iID).fouTriple()==null) {
				tmpMap.put(Math.random(), new Rule(fstTriple, sndTriple));
			}
			
			else if (pRule.get(iID).fouTriple()==null) {
				int a = pRule.get(iID).trdTriple().head();
				int b = pRule.get(iID).trdTriple().tail();
				int c = pRule.get(iID).trdTriple().relation();
				Triple trdTriple = new Triple(a, b, c);
				tmpMap.put(Math.random(), new Rule(fstTriple, sndTriple, trdTriple));
				
			} else {
				
				int a = pRule.get(iID).trdTriple().head();
				int b = pRule.get(iID).trdTriple().tail();
				int c = pRule.get(iID).trdTriple().relation();
				Triple trdTriple = new Triple(a, b, c);
				
				int d = pRule.get(iID).fouTriple().head();
				int e = pRule.get(iID).fouTriple().tail();
				int f = pRule.get(iID).fouTriple().relation();
				Triple fouTriple = new Triple(d, e, f);
				
			}
		}
		
		pRule = new ArrayList<Rule>();
		Iterator<Double> iterValues = tmpMap.keySet().iterator();
		while (iterValues.hasNext()) {
			double dRand = iterValues.next();
			Rule rule = tmpMap.get(dRand);
			int m = rule.fstTriple().head();
			int n = rule.fstTriple().tail();
			int s = rule.fstTriple().relation();
			Triple fstTriple = new Triple(m, n, s);
			int p = rule.sndTriple().head();
			int q = rule.sndTriple().tail();
			int t = rule.sndTriple().relation();
			Triple sndTriple = new Triple(p, q, t);
			
			if(rule.trdTriple()==null && rule.fouTriple()==null) {
				pRule.add(new Rule(fstTriple, sndTriple));
			}
			
			else if (rule.fouTriple()==null){
				int a = rule.trdTriple().head();
				int b = rule.trdTriple().tail();
				int c = rule.trdTriple().relation();
				Triple trdTriple = new Triple(a, b, c);
				pRule.add(new Rule(fstTriple, sndTriple, trdTriple));
			} else {
				int a = rule.trdTriple().head();
				int b = rule.trdTriple().tail();
				int c = rule.trdTriple().relation();
				Triple trdTriple = new Triple(a, b, c);
				
				int d = rule.fouTriple().head();
				int e = rule.fouTriple().tail();
				int f = rule.fouTriple().relation();
				Triple fouTriple = new Triple(d, e, f);
				
				pRule.add(new Rule(fstTriple, sndTriple, trdTriple, fouTriple));
			}
		}
		iNumberOfRules = pRule.size();
		tmpMap.clear();
	}
}
