package kale.joint;

import java.io.File;
import java.util.Scanner;

import basic.util.Arguments;

public class KALEProgram {
	
	public static void main(String[] args) throws Exception {
		
		// train
		// valid
		// test
		// groundings
		// dimension
		// entities
		// relations
		// minibatch
		// m_delta
		// m_gammaE
		// m_gammaR
		// iterations
		// skip
		// m_weight
		
		
		try {
			
			Scanner in = new Scanner(new File("settings.txt"));
			
			String train = in.nextLine();
			String valid = in.nextLine();
			String test = in.nextLine();
			String ground = in.nextLine();
			String ent = in.nextLine();
			String rel = in.nextLine();
			String dim = in.nextLine();
			String mini_batch = in.nextLine();
			String m_d = in.nextLine();
			String m_gE = in.nextLine();
			String m_gR = in.nextLine();
			String iter = in.nextLine();
			String skip = in.nextLine();
			String m_weight = in.nextLine();			
			
			in.close();			
			
			String fnTrainingTriples = train;
			String fnValidateTriples = valid;
			String fnTestingTriples = test;
			String fnTrainingRules = ground;
			String strNumRelation = rel;
			String strNumEntity = ent;
			
			KALEJointModel transe = new KALEJointModel();
			transe.m_NumFactor = Integer.parseInt(dim);
			transe.m_NumMiniBatch = Integer.parseInt(mini_batch);
			transe.m_Delta = Double.parseDouble(m_d);
			transe.m_GammaE = Double.parseDouble(m_gE);
			transe.m_GammaR = Double.parseDouble(m_gR);
			transe.m_NumIteration = Integer.parseInt(iter);
			transe.m_OutputIterSkip = Integer.parseInt(skip);
			transe.m_Weight = Double.parseDouble(m_weight);
			
			System.out.println("Parameters:" +
				"\n\tTrain:" + train +
				"\n\tValid: " + valid +
				"\n\tTest: " + test +
				"\n\tGroundings: " + ground +
				"\n\tEntities: " + ent +
				"\n\tRelations: " + rel +
				"\n\tDimension: " + dim +
				"\n\tNumMiniBatch: " + mini_batch +
				"\n\tMargin: " + m_d +
				"\n\tLearning rate E: " + m_gE +
				"\n\tLearning rate R: " + m_gR +
				"\n\tIterations: " + iter +
				"\n\tOutputIterSkip: " + skip +
				"\n\tWeight: " + m_weight			
				
			);
			
			
			long startTime = System.currentTimeMillis();
			transe.Initialization(strNumRelation, strNumEntity, 
					fnTrainingTriples, fnValidateTriples, fnTestingTriples,
					fnTrainingRules);
			
			System.out.println("\nStart learning KALE-Joint model (triples + rules)");
			transe.TransE_Learn();
			System.out.println("Success.");
			long endTime = System.currentTimeMillis();
			System.out.println("run time:" + (endTime-startTime)+"ms");
			
		} catch(Exception e) {
			
			e.printStackTrace();
			Usage();
		}
		
		
		
		
	}	
	
	
	static void Usage() {
		/*
		System.out.println(
				"Usage: java KALE.jar -train training_triple_path -valid validate_triple_path -test test_triple_path -rule groundings_path -m number_of_relations -n number_of_entities [options]\n\n"
				+

				"Options: \n"
				+ "   -w        -> weights for rules  (default 0.01)\n"
				+ "   -k        -> number of latent factors (default 20)\n"
				+ "   -d        -> value of the margin (default 0.1)\n"
				+ "   -ge       -> learning rate of matrix E (default 0.01)\n"
				+ "   -gr       -> learning rate of tensor R (default 0.01)\n"
				+ "   -#        -> number of iterations (default 1000)\n"
				+ "   -skip     -> number of skipped iterations (default 50)\n"
				);
		*/
		
		System.out.println("Usage: create a file called \"settings.txt\" and put the following parameters:\n" 
				
				+ "train\n"
				+ "valid\n"
				+ "test\n"
				+ "groundings\n"
				+ "dimension\n"
				+ "entities\n"
				+ "relations\n"
				+ "minibatch\n"
				+ "m_delta\n"
				+ "m_gammaE\n"
				+ "m_gammaR\n"
				+ "iterations\n"
				+ "skip\n"
				+ "m_weight"
		);
	}
}
