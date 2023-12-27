package kale.struct;


public class Rule {
	private Triple FstTriple=null;
	private Triple SndTriple=null;
	private Triple TrdTriple=null;
	private Triple FouTriple=null;
	
	public Rule(Triple inFstTriple, Triple inSndTriple) {
		FstTriple = inFstTriple;
		SndTriple = inSndTriple;
	}
	public Rule(Triple inFstTriple, Triple inSndTriple,Triple inTrdTriple) {
		FstTriple = inFstTriple;
		SndTriple = inSndTriple;
		TrdTriple = inTrdTriple;
	}
	
	public Rule(Triple inFstTriple, Triple inSndTriple,Triple inTrdTriple, Triple inFouTriple) {
		FstTriple = inFstTriple;
		SndTriple = inSndTriple;
		TrdTriple = inTrdTriple;
		FouTriple = inFouTriple;
	}
	
	public Triple fstTriple() {
		return FstTriple;
	}
	
	public Triple sndTriple() {
		return SndTriple;
	}
	
	public Triple trdTriple() {
		return TrdTriple;
	}
	
	public Triple fouTriple() {
		return FouTriple;
	}
	
	
}
