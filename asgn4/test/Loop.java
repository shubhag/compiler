public class Loop {

    public static void main(String[] args) {
    int sum,i,j;
    sum = 0;
    i = 1;

    while(i<50)

    {
        sum = sum + i;
        i = i + 1;
    }
    System.out.println(sum);
    System.out.println(i);
    sum = 0;
    i = 1;
    for(i=0;i < 50;i++)
    {
        sum = sum + i;
        i = i + 1;
        if(i>45)
        {
         continue;
        }
        if(i>48)
        {
            break;
        }
        for(j = 1;j < 3;j++)
        {
            System.out.println(j);
            if(j==2){
                break;
            }
        }
    }
    System.out.println(sum);
    System.out.println(i);
    sum = 0;
    i = 1;
    do{
        sum = sum + i;
        i = i + 1;       
    }while(i<50);
    System.out.println(sum);
    System.out.println(i);
    sum = 0;
    i = 1;

}
}