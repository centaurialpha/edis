/*Ejercicio 2. Trabajo practico 4
Bergesio, Florencia MUN° 01173
Fernandez, Gabriel MUN° 01179*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>


typedef struct Nota
{
    char Nombre[50];
    float Nota;
}Nota;


void ordenar (FILE *archivo)
{
   Nota reg,reg2;   //reg es un registro, reg2 es otro registro
   long punt1,punt2;
   fseek(archivo,0,SEEK_END);   //esto lo posiciona al final del archivo

   long cantreg= (ftell(archivo)/sizeof(Nota))-1;  // FTELL te dice cuantos bites hay desde 0 hasta la posicion actual, y lo dividimos en el tamaño del struct, nos dara la cantidad de registros que hay y el -1es por el metodo de la burbuja
   fseek(archivo, 0,SEEK_SET);

  int i=0;
  int j=0;

  while (j<= cantreg -1)
    {
        i=0;
   while (i<=cantreg - j )
   {
     fseek(archivo, i*sizeof(reg),SEEK_SET);
     fread(&reg, sizeof(Nota), 1, archivo); //aca se lee un registro
     fseek(archivo, ((i+1)*sizeof(reg)),SEEK_SET);
     fread(&reg2, sizeof(Nota), 1, archivo);    //aca se lee el registro siguiente al anterior
     if (reg.Nota<reg2.Nota)
    {
          fseek(archivo, i*sizeof(Nota),SEEK_SET);
          fwrite(&reg2, sizeof(Nota), 1, archivo);
          fseek(archivo, ((i+1)*sizeof(reg)),SEEK_SET);
          fwrite(&reg, sizeof(Nota), 1, archivo);
     }
     i=i+1;
   }
   j=j+1;
 }
}


void cargar(FILE *archivo, int contador)
{
    system("cls");
    Nota alumno;
    char respuesta;
    do
    {
    printf("Ingrese el Nombre y apellido del alumno %d\n", contador);
    fflush(stdin);
    gets(alumno.Nombre);
    puts("Ingrese la nota del alumno");
    fflush(stdin);
    scanf("%f", &alumno.Nota);
    printf("Alumno:%s \n",alumno.Nombre);
    printf("Nota %.2f\n", alumno.Nota);
    puts("Esta seguro?");
    fflush(stdin);
    scanf("%c", &respuesta);
    }
    while(respuesta!='s');
        fwrite(&alumno,sizeof(Nota),1,archivo);
        fflush(archivo);
}

void crear(FILE *archivo)
{
    int cantreg=0, contador=1;
    system("cls");
    Nota alumno;
    ordenar(archivo);
    FILE *texto=NULL;
    cantreg=24;
    texto=fopen("calificaciones.txt","wt");
    fprintf(texto,"Nombre:\tNota\n");
    fseek(archivo,sizeof(Nota),SEEK_SET);
    while(contador<=cantreg)
    {
        fread(&alumno,sizeof(Nota),1,archivo);
        fprintf(texto,"%s\t:%.2f\n",alumno.Nombre,alumno.Nota);
        contador++;
    }
    fclose(texto);
    puts("Archivo de texto creado...");
    system("pause");
}

void mostrar(FILE *archivo)
{
    int cantreg=0, contador=1;
   system("cls");
   Nota alumno;
   ordenar(archivo);
   cantreg=24;
   fseek(archivo,sizeof(Nota),SEEK_SET);
   printf("Alumno:  ");
   printf("Nota\n");
   while(contador<=cantreg)
   {
       fread(&alumno,sizeof(Nota),1,archivo);
       printf("%s: ", alumno.Nombre);
       printf(" %.2f\n", alumno.Nota);
       contador++;
   }
   printf("\n");
   system("pause");
}



main()
{
int respuesta;
FILE *archivo=NULL;

archivo=fopen("alumnos.dat","rb+");

if(archivo==NULL)
    {
        do
        {
        printf("Error al abrir el archivo\n");
        printf("Desea crear el archivo?\n");
        printf("1.-Si\n2.-Deseo cerrar el programa\nOpcion:");
        fflush(stdin);
        scanf("%d", &respuesta);
        }
        while(respuesta!=1 && respuesta!=2);
        if(respuesta==1)
            archivo=fopen("alumnos.dat","wb+");
        if(respuesta==2)
            return 0;
    }

while (respuesta!=0 || respuesta<0 || respuesta>3)
{
    system("cls");
    puts("\t\tBienvenido, que desea hacer?\n\n");
    puts("1.- Cargar los 24 alumnos que rindieron el examen\n");
    puts("2.- Mostrar el listado de alumnos ordenado por calificacion\n");
    puts("3.- Generar un archivo llamado calificaciones.txt\n");
    puts("0.- Salir\n");
    printf("Opcion:");
    fflush(stdin);
    scanf("%d",&respuesta);
    switch(respuesta)
    {
    case 1:
        {
            int respuesta1=1;
           do
            {
            system("cls");
            printf("\t\tCargar los 24 alumnos que rindieron el examen\n\n");
            printf("/////////////////////////////////\nNota:si continua, y si el archivo contiene informacion,se sobreescribira\n/////////////////////////////////\n");
            printf("Desea continuar?\n");
            printf("1.-Si\n2.-No\nRespuesta:");
            fflush(stdin);
            scanf("%d",&respuesta1);
            }
            while(respuesta1!=1 && respuesta1!=2);
            if(respuesta1==2)
                break;

            int contador;
            fseek(archivo,sizeof(Nota),SEEK_SET);
            for(contador=1;contador<=24;contador++)
            cargar(archivo, contador);
            break;
        }
    case 2:
        {
            mostrar(archivo);
            break;
        }
    case 3:
        {
            crear(archivo);
            break;
        }
    }
}
fclose(archivo);
}
