# CrazyPAD (Crazyflie <ins>P</ins>ropeller <ins>A</ins>nomaly <ins>D</ins>ata): A dataset for assessing the impact of structural defects on nano-quadcopter performance

<div align="center">
  
| <figure><img src="https://github.com/AerialRoboticsUUST/CrazyPAD/assets/81864311/93cfa246-ea9e-4638-8f7b-c577611a7b16" width="300" alt="Crazyflie"> </figure> | 
|:--:| 
| *Crazyflie 2.1* |
  
</div>

## Data Descriptor Article
>[!NOTE]
>Please, cite our research paper with a detailed description of this dataset:
>
>**Masalimov, K.; Muslimov, T.; Kozlov, E.; Munasypov, R.** *CrazyPAD: A Dataset for Assessing the Impact of Structural Defects on Nano-Quadcopter Performance.* Data 2024, 9, 79. https://doi.org/10.3390/data9060079

## Software solutions are located in the src directory
1. Flight program
2. Scripts for decrypting binary data are located in the decrypt_data directory. The directory contains the readme.md file with a detailed description of the program

## The collected experimental data is presented in the data directory
  - 'add_weight_W1_near_M3_M4' - additional weight W1 is attached to the adhesive tape near the M3 and M4 propellers
  - 'add_weight_W1_near_M3' - additional weight W1 is attached to adhesive tape near the M3 propeller
  - 'add_weight_W1_near_M4' - additional weight W1 is attached to adhesive tape near the M4 propeller
  - 'add_weight_W3_near_M3' - additional weight W3 is attached to adhesive tape near the M3 propeller
  - 'cut_propeller_M3_1mm' - damage to the propeller (length reduction by 1mm) M3
  - 'cut_propeller_M3_2mm' - damage to the propeller (length reduction by 2mm) M3
  - 'cut_propeller_M3_3mm' - damage to the propeller (reduction in length by 3mm) M3
  - 'normal_flight' - flights in normal mode
  - 'tape_on_propeller_M1_M3' - imitation of debris (adhesive tape) sticking to propellers M1 and M3
  - 'tape_on_propeller_M1_M3_M4' - imitation of debris sticking (adhesive tape) on propellers M1 and M3, M4
  - 'tape_on_propeller_M3' - imitation of debris (adhesive tape) sticking to the M3 propeller
  - 'tape_on_propeller_M3_M4' - imitation of debris (adhesive tape) sticking to propellers M3 and M4
  - 'weight_on_string_W2_near_M3' - an additional weight of weight W2 is attached to a 63cm long thread near the M3 propeller
  - 'weight_on_string_W3_near_M3' - an additional weight weighing W3 is attached to a 63cm long thread near the M3 propeller

## Example projects from Bitcraze
[Bitcraze examples](https://github.com/bitcraze/crazyflie-lib-python/tree/master/examples)

## Installing project dependencies
`pip install cflib`
