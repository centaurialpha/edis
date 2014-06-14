/*Ejercicio 1. Trabajo practico 4
Bergesio, Florencia MUN° 01173
Fernandez, Gabriel MUN° 01179*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>



typedef struct fecha
        {
            int dia;
            int mes;
            int anio;
        }fecha;

typedef struct beneficiario
    {
        int registro;
        int validez;
        char nombre[35];
        char barrio[10];
        char direccion[15];
        float ingresos;
        int hijos;
        int documento;
        char sexo;
        int porcentajeAsignado;
        int aporte;
        int estadoCivil; //1 Soltero,2 Casado,3 Viudo,4 Separado Legal,5 Separados de Hecho,6 Divorciado,7 Conviviente//
        fecha fechaNacimiento;
    }beneficiario;

int cantidadreg(FILE *beneficiarios)
{
    int cantreg=0;
    fseek(beneficiarios,0,SEEK_END);
    cantreg=ftell(beneficiarios)/sizeof(beneficiario);
    return cantreg;
}

int verificardni(FILE *beneficiarios,int dni)
{
    beneficiario lectura;
    int bandera=0, contador=0,cantreg=0;
    cantreg=cantidadreg(beneficiarios);
    rewind(beneficiarios);
    while(contador<=cantreg)
    {
        fread(&lectura,sizeof(beneficiario),1,beneficiarios);
        if(lectura.validez==1)
        {
            if(lectura.documento==dni)
                bandera=1;
        }
        contador++;
    }
    return bandera;
}

void agregarBeneficiarios(FILE* beneficiarios,long contadorREGISTRO)
{
    system("cls");
    char opcion;
    int verificar=0;
    beneficiario persona;
    beneficiario lectura;
    fseek(beneficiarios,sizeof(beneficiario),SEEK_END);
    do
    {
    printf("\nNombre beneficiario: ");
    fflush(stdin);
    gets(persona.nombre);
    printf("\nBarrio: ");
    fflush(stdin);
    gets(persona.barrio);
    printf("\nDireccion: ");
    fflush(stdin);
    gets(persona.direccion);
    printf("\nIngresos: ");
    fflush(stdin);
    scanf("%f",&persona.ingresos);
    printf("\nCantidad de Hijos: ");
    fflush(stdin);
    scanf("%d",&persona.hijos);
    do
    {
    printf("\nDNI: ");
    fflush(stdin);
    verificar=0;
    fflush(stdin);
    scanf("%d",&persona.documento);
    verificar=verificardni(beneficiarios,persona.documento);
    }
    while(verificar==1);
    do
    {printf("\nSexo: (H:hombre, M:mujer)");
    fflush(stdin);
    scanf("%s",&persona.sexo);
    }while(persona.sexo!='H'&&persona.sexo!='M');
    printf("\nEstado Civil: \n");
    do
    {puts("1. Soltero/a");
    puts("2. Casado/a");
    puts("3. Viudo/a");
    puts("4. Separado/a Legal");
    puts("5. Separado/a de Hecho");
    puts("6. Divorciado/a");
    puts("7. Conviviente");
    fflush(stdin);
    scanf("%d",&persona.estadoCivil);
    } while(persona.estadoCivil<1||persona.estadoCivil>7);
    puts("Fecha de nacimiento");
    printf("\nDia: ");
    fflush(stdin);
    scanf("%d",&persona.fechaNacimiento.dia);
    printf("\nMes: ");
    fflush(stdin);
    scanf("%d",&persona.fechaNacimiento.mes);
    printf("\nAnio: ");
    fflush(stdin);
    scanf("%d",&persona.fechaNacimiento.anio);
    puts("Los datos ingresados son correctos?(s/n)");
    fflush(stdin);
    scanf("%c",&opcion);
    } while (opcion!='s');
    persona.validez=1;
    persona.registro=ftell(beneficiarios)/sizeof(beneficiario)+1;
    fwrite(&persona,sizeof(beneficiario),1,beneficiarios);
    fflush(beneficiarios);
    system("pause");
}

void gotoxy(int x, int y)
{
COORD coord;
coord.X=x;
coord.Y=y;
SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),coord);
}

void listarBeneficiariosVarones(FILE* beneficiarios)
{
    system("cls");
    beneficiario lectura;
    int contador=2, cont=0, cantreg=0;
    cantreg=cantidadreg(beneficiarios);
    rewind(beneficiarios);
    printf("Nombre");
    gotoxy(41,0);
    printf("|Barrio\n");
    int i;
    for(i=0;i<60;i++)
        printf("_");
    while (cont<cantreg)
    {
    fread(&lectura,sizeof(beneficiario),1,beneficiarios);
    if (lectura.validez!=0)
    {
        if(lectura.sexo=='H')
        {
            if(lectura.ingresos>2500)
            {
                printf("\n%s",lectura.nombre);
                gotoxy(41,contador);
                printf("|%s\n",lectura.barrio);
                ++contador;
            }
        }
    }
    cont++;
    }
    printf("\n");
    system("pause");
}

void cumpleanieros(FILE* beneficiarios)
{
    system("cls");
    int mesCumple,contador=4;
    char continuar;
      do
      {
        puts("Ingrese el numero correspondiente al mes que desea ver.");
        fflush(stdin);
        scanf("%d",&mesCumple);
      }while(mesCumple<1||mesCumple>12);
      beneficiario lectura;
      int cont=0, cantreg=0;
      cantreg=cantidadreg(beneficiarios);
      rewind(beneficiarios);
      gotoxy(0,2);
      printf("Nombre");
        gotoxy(35,2);
        printf("|Direccion");
        gotoxy(52,2);
        printf("|Barrio");
        gotoxy(62,2);
        printf("|Hijos");
        gotoxy(68,2);
        printf("|E. C.");
        gotoxy(80,2);
        printf("|Dia\n");
        int i;
        for(i=0;i<80;i++)
        printf("_");
      while (cont<cantreg)
    {
      fread(&lectura,sizeof(beneficiario),1,beneficiarios);
      if(lectura.validez!=0)
      {
        if(lectura.fechaNacimiento.mes==mesCumple)
        {
            printf("%s",lectura.nombre);
            gotoxy(35,contador);
            printf("|%s",lectura.direccion);
            gotoxy(52,contador);
            printf("|%s",lectura.barrio);
            gotoxy(62,contador);
            printf("|%d",lectura.hijos);
            gotoxy(68,contador);
            switch(lectura.estadoCivil)
            {
                case 1: {puts("|S.");break;}
                case 2: {puts("|C.");break;}
                case 3: {puts("|V.");break;}
                case 4: {puts("|S. L.");break;}
                case 5: {puts("|S. de H.");break;}
                case 6: {puts("|D.");break;}
                case 7: {puts("|Conviv.");break;}
            }
            gotoxy(77,contador);
            printf("|%d",lectura.fechaNacimiento.dia);
            ++contador;
        }
    }
    cont++;
    }
    system("pause");
    system("cls");
}

void listado(FILE* beneficiarios)
{
    int porcentajeIngresos,porcentajeAporte=0,contador=1;
      beneficiario lectura;
      int cont=0,cantreg=0;
      cantreg=cantidadreg(beneficiarios);
      rewind(beneficiarios);
    while (cont<cantreg)
    {
        fread(&lectura,sizeof(beneficiario),1,beneficiarios);
        if (lectura.validez!=0)
        {
            if(lectura.ingresos>=5000) porcentajeIngresos=5;
            if(lectura.ingresos<5000&&lectura.ingresos>=4500) porcentajeIngresos=8;
            if(lectura.ingresos<4500&&lectura.ingresos>=4000) porcentajeIngresos=10;
            if(lectura.ingresos<4000&&lectura.ingresos>=3500) porcentajeIngresos=25;
            if(lectura.ingresos<3500) porcentajeIngresos=35;
            if(lectura.hijos>=3)
            {
                if(lectura.estadoCivil==1||lectura.estadoCivil==3)
                    porcentajeAporte=5;
            }
            printf("\nBeneficiario numero: %d\n",contador);
            printf("\tNombre: "); puts(lectura.nombre);
            printf("\tDocumento: "); printf("%d\n",lectura.documento);
            printf("\tSexo: "); printf("%c\n",lectura.sexo);
            printf("\tIngresos: "); printf("%.2f\n",lectura.ingresos);
            printf("\tPorcentaje asignado: "); printf("%d%%\n",porcentajeIngresos);
            printf("\tHijos: "); printf("%d\n",lectura.hijos);
            printf("\tEstado Civil: ");
            switch(lectura.estadoCivil)
            {
                case 1: {puts("Soltero/a");break;}
                case 2: {puts("Casado/a");break;}
                case 3: {puts("Viudo/a");break;}
                case 4: {puts("S. Legal");break;}
                case 5: {puts("S. de Hecho");break;}
                case 6: {puts("Divorciado/a");break;}
                case 7: {puts("Conviviente");break;}
            }
            printf("\n\tAporte: "); printf("%d%%",porcentajeAporte);
            contador++;
        }
        cont++;
    }
    puts(" ");
    system("pause");
}

void darBaja(FILE* beneficiarios)
{
    int dni;
    char borrar;
    beneficiario lectura;
    puts("Ingrese el numero de DNI del beneficiario a dar de baja");
    fflush(stdin);
    scanf("%d",&dni);
    int cont=1,cantreg=0,bandera=0;
    cantreg=cantidadreg(beneficiarios);
    rewind(beneficiarios);
    while(cont<=cantreg)
    {
        fread(&lectura,sizeof(beneficiario),1,beneficiarios);
        if(lectura.validez==1&&dni==lectura.documento)
        {
            bandera=1;
            printf("Nombre:");printf(" %s\n",lectura.nombre);
            printf("D.N.I:");printf(" %d\n",lectura.documento);
            printf("Sexo:");printf(" %c\n",lectura.sexo);
                printf("\nEs este el beneficiario al que quiere dar de baja? (s/n)\n");
                fflush(stdin);
                scanf("%c",&borrar);
                if(borrar=='s')
                {
                lectura.validez=0;
                fseek(beneficiarios,(lectura.registro-1)*sizeof(beneficiario),SEEK_SET);
                fwrite(&lectura,sizeof(beneficiario),1,beneficiarios);
                return 0;
                }
                else
                    return 0;

        }
    cont++;
    }
    if(bandera==0)
    printf("Persona no encontrada\n");
    system("pause");

}

int menu(FILE* beneficiarios,long contadorREGISTRO)
{
    system("cls");
    int opcion;
    do
    {
        puts("1. Agregar beneficiarios.");
        puts("2. Beneficiarios varones con ingresos mayores a $2500.");
        puts("3. Listado cumpleañeros por mes.");
        puts("4. Listado por beneficiario.");
        puts("5. Dar de baja a beneficiarios.");
        puts("0. Salir.\n\n");
        puts("Opcion: ");
        fflush(stdin);
        scanf("%d",&opcion);
    }while (opcion<0||opcion>5);
    switch (opcion)
    {
    case 1:
        {agregarBeneficiarios(beneficiarios,contadorREGISTRO);break;}
    case 2:
        {listarBeneficiariosVarones(beneficiarios);break;}
    case 3:
        {cumpleanieros(beneficiarios);break;}
    case 4:
        {listado(beneficiarios);break;}
    case 5:
        {darBaja(beneficiarios);break;}
    case 0:
        {return 999;break;}
    }
}
long Filesize(FILE*beneficiarios)
{
    long posi,largo;
    posi=ftell(beneficiarios);
    fseek(beneficiarios,0L,SEEK_END);
    largo=ftell(beneficiarios);
    fseek(beneficiarios,posi,SEEK_SET);
    return largo;
}

main()
{
    FILE* beneficiarios;
    int aux;
    beneficiarios=fopen("Beneficiarios.ben","rb+");
    if(beneficiarios==NULL)
    {
        beneficiarios=fopen("Beneficiarios.ben","wb+");
    }
    rewind(beneficiarios);
    long largoArchivo=Filesize(beneficiarios);
    long largoStruct=sizeof(struct beneficiario);
    long contadorREGISTRO=largoArchivo/largoStruct;
    rewind(beneficiarios);
    do{
    aux=menu(beneficiarios,contadorREGISTRO);
    }while (aux!=999);
    fclose(beneficiarios);
    puts(" ");
    return 0;
}
