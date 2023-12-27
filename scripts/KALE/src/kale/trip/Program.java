package kale.trip;

import java.io.File;
import java.util.Scanner;

import basic.util.Arguments;
import kale.joint.KALEJointModel;

public class Program {
	
	public static void main(String[] args) throws Exception {
		
		try {
			
Scanner in = new Scanner(new File("settings.txt"));
			
			String train = in.nextLine();
			String valid = in.nextLine();
			String test = in.nextLine();
			String ent = in.nextLine();
			String rel = in.nextLine();
			String dim = in.nextLine();
			String mini_batch = in.nextLine();
			String m_d = in.nextLine();
			String m_gE = in.nextLine();
			String m_gR = in.nextLine();
			String iter = in.nextLine();
			String skip = in.nextLine();		
			
			in.close();			
			
			String fnTrainingTriples = train;
			String fnValidateTriples = valid;
			String fnTestingTriples = test;
			String strNumRelation = rel;
			String strNumEntity = ent;
			
			KALETripModel transe = new KALETripModel();
			transe.m_NumFactor = Integer.parseInt(dim);
			transe.m_NumMiniBatch = Integer.parseInt(mini_batch);
			transe.m_Delta = Double.parseDouble(m_d);
			transe.m_GammaE = Double.parseDouble(m_gE);
			transe.m_GammaR = Double.parseDouble(m_gR);
			transe.m_NumIteration = Integer.parseInt(iter);
			transe.m_OutputIterSkip = Integer.parseInt(skip);
			
			System.out.println("Parameters:" +
				"\n\tTrain:" + train +
				"\n\tValid: " + valid +
				"\n\tTest: " + test +
				"\n\tEntities: " + ent +
				"\n\tRelations: " + rel +
				"\n\tDimension: " + dim +
				"\n\tNumMiniBatch: " + mini_batch +
				"\n\tMargin: " + m_d +
				"\n\tLearning rate E: " + m_gE +
				"\n\tLearning rate R: " + m_gR +
				"\n\tIterations: " + iter +
				"\n\tOutputIterSkip: " + skip	
				
			);
			
			long startTime = System.currentTimeMillis();
			transe.Initialization(strNumRelation, strNumEntity, fnTrainingTriples, fnValidateTriples, fnTestingTriples);
			
			System.out.println("\nStart learning TransE-linear model (triples only)");
			transe.TransE_Learn();
			System.out.println("Success.");
			long endTime = System.currentTimeMillis();
			System.out.println("run time:" + (endTime-startTime)+"ms");
			
		} catch(Exception e) {
			
			e.printStackTrace();
			Usage();
		}
		
	}
	
	/*
	public static void main(String[] args) throws Exception {
		Arguments cmmdArg = new Arguments(args);
		/*
		KALETripModel transe = new KALETripModel();
		String fnTrainingTriples = "datasets\\uniba\\train.txt";
		String fnValidateTriples = "datasets\\uniba\\valid.txt";
		String fnTestingTriples = "datasets\\uniba\\test.txt";
		String strNumRelation = "1";
		String strNumEntity = "9132";
		*/ /*
		
		KALETripModel transe = new KALETripModel();
		String fnTrainingTriples = "datasets//dbpedia_useritem//train.txt";
		String fnValidateTriples = "datasets//dbpedia_useritem//valid.txt";
		String fnTestingTriples = "datasets//dbpedia_useritem//test.txt";
		String strNumRelation = "1";
		String strNumEntity = "9130";
		
		long startTime = System.currentTimeMillis();
		transe.Initialization(strNumRelation, strNumEntity, fnTrainingTriples, fnValidateTriples, fnTestingTriples);
		
		System.out.println("\nStart learning TransE-linear model (triples only)");
		transe.TransE_Learn();
		System.out.println("Success.");
		long endTime = System.currentTimeMillis();
		System.out.println("run time:" + (endTime-startTime)+"ms");
		
	}
*/
	
	/*
	public static void main(String[] args) throws Exception {
		Arguments cmmdArg = new Arguments(args);
		KALETripModel transe = new KALETripModel();
		String fnTrainingTriples = "";
		String fnValidateTriples = "";
		String fnTestingTriples = "";
		String strNumRelation = "";
		String strNumEntity = "";
		
		try {
			fnTrainingTriples = cmmdArg.getValue("train");
			if (fnTrainingTriples == null || fnTrainingTriples.equals("")) {
				Usage();
				return;
			}
			fnValidateTriples = cmmdArg.getValue("valid");
			if (fnValidateTriples == null || fnValidateTriples.equals("")) {
				Usage();
				return;
			}
			fnTestingTriples = cmmdArg.getValue("test");
			if (fnTestingTriples == null || fnTestingTriples.equals("")) {
				Usage();
				return;
			}
			strNumRelation = cmmdArg.getValue("m");
			if (strNumRelation == null || strNumRelation.equals("")) {
				Usage();
				return;
			}
			strNumEntity = cmmdArg.getValue("n");
			if (strNumEntity == null || strNumEntity.equals("")) {
				Usage();
				return;
			}
			
			if (cmmdArg.getValue("k") != null && !cmmdArg.getValue("k").equals("")) {
				transe.m_NumFactor = Integer.parseInt(cmmdArg.getValue("k"));
			}
			if (cmmdArg.getValue("d") != null && !cmmdArg.getValue("d").equals("")) {
				transe.m_Delta = Double.parseDouble(cmmdArg.getValue("d"));
			}
			if (cmmdArg.getValue("ge") != null && !cmmdArg.getValue("ge").equals("")) {
				transe.m_GammaE = Double.parseDouble(cmmdArg.getValue("ge"));
			}
			if (cmmdArg.getValue("gr") != null && !cmmdArg.getValue("gr").equals("")) {
				transe.m_GammaR = Double.parseDouble(cmmdArg.getValue("gr"));
			}
			if (cmmdArg.getValue("#") != null && !cmmdArg.getValue("#").equals("")) {
				transe.m_NumIteration = Integer.parseInt(cmmdArg.getValue("#"));
			}
			if (cmmdArg.getValue("skip") != null && !cmmdArg.getValue("skip").equals("")) {
				transe.m_OutputIterSkip = Integer.parseInt(cmmdArg.getValue("skip"));
			}

			long startTime = System.currentTimeMillis();
			transe.Initialization(strNumRelation, strNumEntity, fnTrainingTriples, fnValidateTriples, fnTestingTriples);
			
			System.out.println("\nStart learning TransE-linear model (triples only)");
			transe.TransE_Learn();
			System.out.println("Success.");
			long endTime = System.currentTimeMillis();
			System.out.println("run time:" + (endTime-startTime)+"ms");
		} catch (Exception e) {
			e.printStackTrace();
			Usage();
			return;
		}
	}
	*/
	
	static void Usage() {
		System.out.println(
				"Usagelala: java TransE -t training_triples -v validate_triples -m number_of_relations -n number_of_entities [options]\n\n"
				+

				"Options: \n"
				+ "   -k        -> number of latent factors (default 20)\n"
				+ "   -d        -> value of the margin (default 0.1)\n"
				+ "   -ge       -> learning rate of matrix E (default 0.01)\n"
				+ "   -gr       -> learning rate of tensor R (default 0.01)\n"
				+ "   -#        -> number of iterations (default 1000)\n"
				+ "   -skip     -> number of skipped iterations (default 50)\n"
				);
	}
}
