/*Ejercicio 3. Trabajo practico 4
Bergesio, Florencia MUN° 01173
Fernandez, Gabriel MUN° 01179*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>


typedef struct
{
    int zona;
    char sexo;
    int edad;
    char producto;
}Producto;

void agregar(FILE *archivo)
{
    int resp=3, resp1;
    Producto persona;
    fseek(archivo,0,SEEK_END);
    while(resp!=1)
      {
    persona.zona=-1;
    persona.sexo='P';
    persona.edad=-1;
    persona.producto='P';
    system("cls");
        while(persona.zona<1||persona.zona>30)
        {
            puts("Ingrese la zona a la que pertenece el encuestado");
            fflush(stdin);
            scanf("%d",&persona.zona);
        }
        while(persona.sexo!='H'&&persona.sexo!='M')
        {
            puts("Ingrese el sexo del encuestado (M=mujer;H=hombre)");
            fflush(stdin);
            scanf("%c",&persona.sexo);
        }
        while(persona.edad<1)
        {
            puts("Ingrese la edad del encuestado");
            fflush(stdin);
            scanf("%d",&persona.edad);
        }
        while(persona.producto!='A'&&persona.producto!='B'&&persona.producto!='C'&&persona.producto!='D'&&persona.producto!='E'&&persona.producto!='F')
        {
            puts("Ingrese el producto de preferencia del encuestado(A,B,C,D,E,F)");
            fflush(stdin);
            scanf("%c",&persona.producto);
        }
        resp1=3;
        while(resp1!=1&&resp1!=2)
        {
            puts("los datos ingresados, son correctos?");
            puts("1.-Si");
            puts("2.-No");
            fflush(stdin);
            scanf("%d",&resp1);
            resp=resp1;
        }
     }
     fwrite(&persona,sizeof(Producto),1,archivo);
}

int mostprodmay(FILE *archivo)
{
    Producto prod;
    int cantreg=0, contador=0;
    int contA=0,contB=0,contC=0,contD=0,contE=0,contF=0, mayor=-1;
    char may='G';
    fseek(archivo,0,SEEK_END);
    cantreg=ftell(archivo)/sizeof(Producto);
    rewind(archivo);
    while(contador<cantreg)
    {
        fread(&prod,sizeof(Producto),1,archivo);
        switch(prod.producto)
        {
        case 'A':
            {
               contA=contA+1;
               break;
            }
        case 'B':
            {
                contB=contB+1;
                break;
            }
        case 'C':
            {
                contC=contC+1;
                break;
            }
        case 'D':
            {
                contD=contD+1;
                break;
            }
        case 'E':
            {
                contE=contE+1;
                break;
            }
        case 'F':
            {
                contF=contF+1;
                break;
            }
        }
        contador++;
    }

    if(mayor<contA)
    {
    mayor=contA;
    may='A';
    }
    if(mayor<contB)
    {
    mayor=contB;
    may='B';
    }
    if(mayor<contC)
    {
    mayor=contC;
    may='C';
    }
    if(mayor<contD)
    {
    mayor=contD;
    may='D';
    }
        if(mayor<contE)
    {
    mayor=contE;
    may='E';
    }
        if(mayor<contF)
    {
    mayor=contF;
    may='F';
    }

    printf("El producto con mas adherentes es el producto %c con un total de %d\n",may,mayor);
    return may;
}

void mostcantmujmay(FILE *archivo, char prod)
{
    int cantreg=0, contador=0, contar=0;
    Producto leer;
    fseek(archivo,0,SEEK_END);
    cantreg=ftell(archivo)/sizeof(Producto);
    rewind(archivo);
    fread(&leer,sizeof(Producto),1,archivo);
    while(contador<cantreg)
    {
        fread(&leer,sizeof(Producto),1,archivo);
        if(leer.sexo=='M'&&leer.producto==prod)
        {
                contar++;
        }
        contador++;
    }
    printf("La cantidad de mujeres que eligieron el producto %c es de %d\n",prod,contar);
}

int menu()
{
    system("cls");
    int respuesta=-1;
    while(respuesta<0||respuesta>7)
    {
        printf("\t\t\t BIENVENIDO al programa de encuesta\n\n");
        puts("1.-Ingresar los datos de un encuestado");
        puts("2.-Mostrar producto con mayor cantidad de adherentes");
        puts("3.-Mostrar cantidad de mujeres que optaron por el producto ganador");
        puts("4.-Mostrar el porcentaje de adherentes para cada producto");
        puts("5.-Mostrar rango de las edades de los encuestados(la mayor y menor edad)");
        puts("6.-Promedio de edad del producto ganador");
        puts("7.-Cantidad de personas que optaron por el producto D en cada zona");
        puts("0.-Salir.");
        fflush(stdin);
        scanf("%d", &respuesta);
    }
    return respuesta;
}

void porccadaprod(FILE *archivo)
{
    Producto leer;
    int total=0,contador=0,contA=0,contB=0,contC=0,contD=0,contE=0,contF=0;
    float porcA,porcB,porcC,porcD,porcE,porcF;
    fseek(archivo,0,SEEK_END);
    total=ftell(archivo)/sizeof(Producto);
    rewind(archivo);
    while(contador<total)
    {
        fread(&leer,sizeof(Producto),1,archivo);
        switch(leer.producto)
        {
        case 'A':
            {
               contA=contA+1;
               break;
            }
        case 'B':
            {
                contB=contB+1;
                break;
            }
        case 'C':
            {
                contC=contC+1;
                break;
            }
        case 'D':
            {
                contD=contD+1;
                break;
            }
        case 'E':
            {
                contE=contE+1;
                break;
            }
        case 'F':
            {
                contF=contF+1;
                break;
            }
        }
        contador++;
    }
    porcA=contA*100/total;
    porcB=contB*100/total;
    porcC=contC*100/total;
    porcD=contD*100/total;
    porcE=contE*100/total;
    porcF=contF*100/total;

    printf("El procentaje de encuestados que opto por el producto A es %.2f%%\n",porcA);
    printf("El procentaje de encuestados que opto por el producto B es %.2f%%\n",porcB);
    printf("El procentaje de encuestados que opto por el producto C es %.2f%%\n",porcC);
    printf("El procentaje de encuestados que opto por el producto D es %.2f%%\n",porcD);
    printf("El procentaje de encuestados que opto por el producto E es %.2f%%\n",porcE);
    printf("El procentaje de encuestados que opto por el producto F es %.2f%%\n",porcF);
}

void rangedad(FILE *archivo)
{
    Producto leer;
    int cantreg=0,contador=0,MAX=0,MIN=999;
    fseek(archivo,0,SEEK_END);
    cantreg=ftell(archivo)/sizeof(Producto);
    rewind(archivo);
    while(contador<cantreg)
    {
        fread(&leer,sizeof(Producto),1,archivo);
        if(leer.edad<MIN)
            MIN=leer.edad;
        contador++;
    }
        contador=0;
        while(contador<cantreg)
    {
        fread(&leer,sizeof(Producto),1,archivo);
        if(leer.edad>MAX)
            MAX=leer.edad;
        contador++;
    }
    printf("En las encuestas, el rango de edad es de (%d--%d)\n",MIN,MAX);
}

void promedadmay(FILE *archivo,char prod)
{
    Producto leer;
    int total=0,cantreg=0,contador=0,promedio=0,acumulador=0;
    fseek(archivo,0,SEEK_END);
    cantreg=ftell(archivo)/sizeof(Producto);
    rewind(archivo);
    while(contador<cantreg)
    {
        fread(&leer,sizeof(Producto),1,archivo);
        if(leer.producto==prod)
        {
            total++;
            acumulador=acumulador+leer.edad;
        }
        contador++;
    }
    promedio=acumulador/total;
    printf("La edad promedio de los encuestados que eligieron el producto %c es %d\n",prod,promedio);
}

void cantpersD(FILE *archivo)
{
    Producto leer;
    int zona=1, contador=0, cantreg=0,contar=0;
    fseek(archivo,0,SEEK_END);
    cantreg=ftell(archivo)/sizeof(Producto);
    rewind(archivo);
    while(zona<=30)
    {
        rewind(archivo);
        contar=0;
        contador=0;
        while(contador<cantreg)
        {
            fread(&leer,sizeof(Producto),1,archivo);
            if(leer.producto=='D'&&leer.zona==zona)
            {
               contar++;
            }
            contador++;
        }
        printf("La cantidad de personas que prefieren el producto D en la Zona %d es de:%d\n",zona,contar);
    zona++;
    }
    system("pause");
}

main()
{
    FILE *producto=NULL;
    char mayprod;
    producto=fopen("producto.gf","rb+");
    if(producto==NULL)
    {
        int resp=3;
        puts("Archivo no encontrado, desea crearlo?");
        puts("1.-Si");
        puts("2.-Salir del programa");
        while(resp!=1&&resp!=2)
        {
            printf("Opcion:");
            fflush(stdin);
            scanf("%d",&resp);
        }
        if(resp==2)
            return 0;
        if(resp==1)
            producto=fopen("producto.gf","wb+");
    }

    int respuesta=1;
    while(respuesta!=0)
    {
        respuesta=menu();
        switch (respuesta)
        {
        case 0:
            return 0;

        case 1:
            {
                system("cls");
                agregar(producto);
                system("pause");
                system("cls");
                break;
            }
        case 2:
            {
                system("cls");
                mayprod=mostprodmay(producto);
                system("pause");
                system("cls");
                break;
            }
        case 3:
            {
                system("cls");
                mayprod=mostprodmay(producto);
                system("cls");
                mostcantmujmay(producto,mayprod);
                system("pause");
                system("cls");
                break;
            }
        case 4:
            {
                system("cls");
                porccadaprod(producto);
                system("pause");
                system("cls");
                break;
            }
        case 5:
            {
                system("cls");
                rangedad(producto);
                system("pause");
                system("cls");
                break;
            }
        case 6:
            {
                system("cls");
                mayprod=mostprodmay(producto);
                system("cls");
                promedadmay(producto, mayprod);
                system("pause");
                system("cls");
                break;
            }
        case 7:
            {
                cantpersD(producto);
                break;
            }
        }
    }
    fclose(producto);
}
