I file `.jar` contenuti di default in questa cartella sono stati esportati dal progetto [KALE](../../../src/kale).

| File                      | Classe                                        | Parametri (in ordine)                 |
| -------------------------:|:---------------------------------------------:|:-------------------------------------:|  
| `ConvertDataForm.jar` | [`ConvertDataForm2.java`](../../../src/kale/src/basic/dataProcess/ConvertDataForm2.java) |  `INPUT_KALE_TRAIN_PATH`, `INPUT_KALE_VALID_PATH`, `INPUT_KALE_TEST_PATH`, `OUTPUT_TRAIN_PATH`, `OUTPUT_VALID_PATH`, `OUTPUT_TEST_PATH`, `OUTPUT_ENTITY_ID_PATH`, `OUTPUT_RELATION_ID_PATH` |
| `GroundAllRules.jar` | [`NewGroundAllRules2.java`](../../../src/kale/src/basic/dataProcess/NewGroundAllRules2.java) | `INPUT_RELATION_ID_PATH`, `INPUT_TRAIN_PATH`, `INPUT_RULES_PATH`, `OUTPUT_GROUNDINGS_PATH` |
| `KALEJointProgram.jar` | [`KALEProgram2.java`](../../../src/kale/src/kale/joint/KALEProgram2.java) | `INPUT_TRAIN_PATH`, `INPUT_VALID_PATH`, `INPUT_TEST_PATH`, `INPUT_GROUNDINGS_PATH`, `OUTPUT_MATRIX_E_PATH`, `OUTPUT_MATRIX_R_PATH`, `OUTPUT_KALE_LOGS_PATH`, `ENTITIES_COUNT`, `RELATIONS_COUNT`, `EMBEDDING_DIMENSION`, `MINI_BATCH`, `M_D`, `M_GE`, `M_GR`, `ITERATIONS`, `SKIP`, `WEIGHT` |
| `KALETripProgram.jar` | [`Program2.java`](../../../src/kale/src/kale/trip/Program2.java) | `INPUT_TRAIN_PATH`, `INPUT_VALID_PATH`, `INPUT_TEST_PATH`, `OUTPUT_MATRIX_E_PATH`, `OUTPUT_MATRIX_R_PATH`, `OUTPUT_KALE_LOGS_PATH`, `ENTITIES_COUNT`, `RELATIONS_COUNT`, `EMBEDDING_DIMENSION`, `MINI_BATCH`, `M_D`, `M_GE`, `M_GR`, `ITERATIONS`, `SKIP` |

Questi `.jar` prendono in input così tanti percorsi per fare in modo che l'unica autorità sulla posizione dei file sia [`paths.py`](../paths.py). I vari script Python determinano le posizioni dei file di input e di output e comunicano queste informazioni alle componenti scritte in Java, tramite i parametri posizionali descritti nella tabella. In questo modo, non c'è bisogno di modificare anche le componenti Java se si decide di cambiare i percorsi o i nomi dei file e delle cartelle.

Possibili alternative:
* Server locale che offre i servizi di `paths.py` anche alle componenti scritte in Java.
* Processo demone che offre i servizi di `paths.py` anche alle componenti scritte in Java.
* Riscrivere queste componenti in Python.