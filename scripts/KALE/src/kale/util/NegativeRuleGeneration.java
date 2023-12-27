package kale.util;

import java.util.ArrayList;
import java.util.HashMap;

import kale.struct.Rule;
import kale.struct.Triple;

public class NegativeRuleGeneration {
	public Rule PositiveRule;
	public int iNumberOfRelations;
	
	public NegativeRuleGeneration(Rule inPositiveRule,
			int inNumberOfRelations) {
		PositiveRule = inPositiveRule;
		iNumberOfRelations = inNumberOfRelations;
	}
	
	public Rule generateSndNegRule() throws Exception {
		
		if(PositiveRule.trdTriple()==null){
			Triple fstTriple = PositiveRule.fstTriple();
			int iSndHead = PositiveRule.sndTriple().head();
			int iSndTail = PositiveRule.sndTriple().tail();
			int iSndRelation = PositiveRule.sndTriple().relation();
			int iFstRelation = PositiveRule.fstTriple().relation();
			
			int iNegRelation = iSndRelation;
			Triple sndTriple = new Triple(iSndHead, iSndTail, iNegRelation);
			while (iNegRelation == iSndRelation || iNegRelation == iFstRelation) {
				iNegRelation = (int)(Math.random() * iNumberOfRelations);
				sndTriple = new Triple(iSndHead, iSndTail, iNegRelation);
			}
			Rule NegativeRule = new Rule(fstTriple, sndTriple);
			return NegativeRule;
		}
		else if (PositiveRule.fouTriple() == null){
			
			Triple fstTriple = PositiveRule.fstTriple();
			Triple sndTriple = PositiveRule.sndTriple();
			int iTrdHead = PositiveRule.trdTriple().head();
			int iTrdTail = PositiveRule.trdTriple().tail();
			int iTrdRelation = PositiveRule.trdTriple().relation();
			int iFstRelation = PositiveRule.fstTriple().relation();
			int iSndRelation = PositiveRule.sndTriple().relation();
			
			int iNegRelation = iTrdRelation;
			Triple trdTriple = new Triple(iTrdHead, iTrdTail, iNegRelation);
			while (iNegRelation == iTrdRelation || iNegRelation == iSndRelation || iNegRelation == iFstRelation) {
				iNegRelation = (int)(Math.random() * iNumberOfRelations);
				trdTriple = new Triple(iTrdHead, iTrdTail, iNegRelation);
			}
			Rule NegativeRule = new Rule(fstTriple, sndTriple, trdTriple);
			return NegativeRule;
		}
		else{
			
			
			Triple fstTriple = PositiveRule.fstTriple();
			Triple sndTriple = PositiveRule.sndTriple();
			Triple trdTriple = PositiveRule.trdTriple();
			
			int iFouHead = PositiveRule.fouTriple().head();
			int iFouTail = PositiveRule.fouTriple().tail();
			int iFouRelation = PositiveRule.fouTriple().relation();
			int iTrdRelation = PositiveRule.trdTriple().relation();
			int iSndRelation = PositiveRule.sndTriple().relation();
			int iFstRelation = PositiveRule.fstTriple().relation();
			
			int iNegRelation = iFouRelation;
			Triple fouTriple = new Triple(iFouHead, iFouTail, iNegRelation);
			
			while (iNegRelation == iTrdRelation 
					|| iNegRelation == iSndRelation 
					|| iNegRelation == iFstRelation
					|| iNegRelation == iFouRelation) {
				
				iNegRelation = (int)(Math.random() * iNumberOfRelations);
				fouTriple = new Triple(iFouHead, iFouTail, iNegRelation);
				
			}
			
			Rule NegativeRule = new Rule(fstTriple, sndTriple, trdTriple, fouTriple);
			return NegativeRule;
		}
		
	}
	
	/*
	public Rule generateFstNegRule() throws Exception {
		Triple sndTriple = PositiveRule.sndTriple();
		int ifstHead = PositiveRule.fstTriple().head();
		int ifstTail = PositiveRule.fstTriple().tail();
		int iFstRelation = PositiveRule.fstTriple().relation();
		int iSndRelation = PositiveRule.sndTriple().relation();
		
		int iNegRelation = iFstRelation;
		Triple fstTriple = new Triple(ifstHead, ifstTail, iNegRelation);
		while (iNegRelation == iSndRelation || iNegRelation == iFstRelation) {
			iNegRelation = (int)(Math.random() * iNumberOfRelations);
			fstTriple = new Triple(ifstHead, ifstTail, iNegRelation);
		}
		Rule NegativeRule = new Rule(fstTriple, sndTriple);
		return NegativeRule;
	}
	*/
	
	public Rule generateFstNegRule() throws Exception {
		
		if(PositiveRule.trdTriple()==null){
			Triple fstTriple = PositiveRule.fstTriple();
			int iSndHead = PositiveRule.sndTriple().head();
			int iSndTail = PositiveRule.sndTriple().tail();
			int iSndRelation = PositiveRule.sndTriple().relation();
			int iFstRelation = PositiveRule.fstTriple().relation();
			
			int iNegRelation = iSndRelation;
			Triple sndTriple = new Triple(iSndHead, iSndTail, iNegRelation);
			while (iNegRelation == iSndRelation || iNegRelation == iFstRelation) {
				iNegRelation = (int)(Math.random() * iNumberOfRelations);
				sndTriple = new Triple(iSndHead, iSndTail, iNegRelation);
			}
			Rule NegativeRule = new Rule(fstTriple, sndTriple);
			return NegativeRule;
		}
		else if (PositiveRule.fouTriple() == null){
			
			Triple fstTriple = PositiveRule.fstTriple();
			Triple sndTriple = PositiveRule.sndTriple();
			int iTrdHead = PositiveRule.trdTriple().head();
			int iTrdTail = PositiveRule.trdTriple().tail();
			int iTrdRelation = PositiveRule.trdTriple().relation();
			int iFstRelation = PositiveRule.fstTriple().relation();
			int iSndRelation = PositiveRule.sndTriple().relation();
			
			int iNegRelation = iTrdRelation;
			Triple trdTriple = new Triple(iTrdHead, iTrdTail, iNegRelation);
			while (iNegRelation == iTrdRelation || iNegRelation == iSndRelation || iNegRelation == iFstRelation) {
				iNegRelation = (int)(Math.random() * iNumberOfRelations);
				trdTriple = new Triple(iTrdHead, iTrdTail, iNegRelation);
			}
			Rule NegativeRule = new Rule(fstTriple, sndTriple, trdTriple);
			return NegativeRule;
		}
		else{
			
			
			Triple fstTriple = PositiveRule.fstTriple();
			Triple sndTriple = PositiveRule.sndTriple();
			Triple trdTriple = PositiveRule.trdTriple();
			
			int iFouHead = PositiveRule.fouTriple().head();
			int iFouTail = PositiveRule.fouTriple().tail();
			int iFouRelation = PositiveRule.fouTriple().relation();
			int iTrdRelation = PositiveRule.trdTriple().relation();
			int iSndRelation = PositiveRule.sndTriple().relation();
			int iFstRelation = PositiveRule.fstTriple().relation();
			
			int iNegRelation = iFouRelation;
			Triple fouTriple = new Triple(iFouHead, iFouTail, iNegRelation);
			
			while (iNegRelation == iTrdRelation 
					|| iNegRelation == iSndRelation 
					|| iNegRelation == iFstRelation
					|| iNegRelation == iFouRelation) {
				
				iNegRelation = (int)(Math.random() * iNumberOfRelations);
				fouTriple = new Triple(iFouHead, iFouTail, iNegRelation);
				
			}
			
			Rule NegativeRule = new Rule(fstTriple, sndTriple, trdTriple, fouTriple);
			return NegativeRule;
		}


	}
	
}
