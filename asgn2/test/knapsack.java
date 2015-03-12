import java.io.*;
import java.util.*;

class Knapsack
{
   public static void main (String args[]) // entry point from OS
   {
      new MyClass(new Scanner(System.in));  // create dynamic entry point
   }
}

class MyClass {

   MyClass (Scanner s)
   {
      Scanner ls;
      int B[][];
      int numItems, maxWeight, w, k;
      int benefit[], weight[];
      int remainingWeight;
      int setNumber = 1;

    //***  Read in the initial numItems, maxWeight pair
      ls = new Scanner(s.nextLine());
      numItems = ls.nextInt();
      maxWeight = ls.nextInt();
 
    while ( (numItems != 0) && (maxWeight != 0) )
    {
      // *** Read in all the data for the items
          benefit = new int [numItems+1];
          weight = new int [numItems+1];
          ls = new Scanner(s.nextLine());
          for (k = 1; k <= numItems; k++)
              {  
                  benefit [k] = ls.nextInt();
                  weight [k] = ls.nextInt();
              }

      // *** initialize
          B = new int [numItems+1][maxWeight+1]; 
          for (w = 0; w <= maxWeight; w++) 
                    B[0][w] = 0; 

      // *** Now do the work!
          for (k = 1; k <= numItems; k++)
              {
                  for (w = maxWeight; w >= weight[k]; w--)
                      if (benefit[k] + B[k-1][w-weight[k]] > B[k-1][w])
                         B[k][w] = benefit[k] + B[k-1][w-weight[k]];
                      else
                         B[k][w] = B[k-1][w];
                  for (w = 0; w < weight[k]; w++)
                         B[k][w] = B[k-1][w];
              }

      // *** Print out the results.   
          System.out.println("Set #" + setNumber);
          System.out.println("Max benefit = " + B[numItems][maxWeight]);
          System.out.print("Items used:");
          for (k = numItems, remainingWeight=maxWeight; k > 0; k--)
              {
                if (remainingWeight >= weight[k])
                   if ( B[k][remainingWeight] == (benefit[k] + B[k-1][remainingWeight - weight[k]]) )
                    {
                       System.out.print("  " + k);
                       remainingWeight -= weight[k];
                    }
              }
              System.out.println();
              System.out.println();
              setNumber++;

      // ***  Read in the next numItems, maxWeight pair
      ls = new Scanner(s.nextLine());
      numItems = ls.nextInt();
      maxWeight = ls.nextInt();
   }  
 
 }
}