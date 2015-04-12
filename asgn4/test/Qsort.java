class Qsort
{
	public static int quicksort(int[] x, int first, int last){
		int pivot,j,temp,i,f,e,a;
		// System.out.println(last);
		// a = 123;
		// System.out.println(a);
		// System.out.println(first);
		System.out.println(last);

		if(first<last){
			pivot=first;
			i=first;
			j=last;
			// System.out.println(1234567);
			while(i<j){
				while((x[i] <= x[pivot]) && (i < last)){
					i++;
				}
				while(x[j]>x[pivot]){
					j--;
				}
				if(i<j){
					temp=x[i];
					x[i]=x[j];
					x[j]=temp;
				}
			}

			temp=x[pivot];
			x[pivot]=x[j];
			x[j]=temp;
			f = j -1 ;
			e = j + 1;
			quicksort(x,first,f);
			quicksort(x,e,last);

		}
		return 0;
	}

	public static void main(String[] args){
		int[] x = new int[5];
		int size = 5;
		int first = 0;
		int l = size - 1;
		int i;

		for(i=0;i<size;i++){
			x[i] = 100-i;
		}
		// for(i=0;i<size;i++){
			System.out.println(l);
		// }
		quicksort(x,first,l);

		for(i=0;i<size;i++){
			System.out.println(x[i]);
		}
	}

}