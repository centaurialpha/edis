sadasd/*Ejercicio 4. Trabajo practico 4
Bergesio, Florencia MUN° 01173
Fernandez, Gabriel MUN° 01179*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

typedef struct stock
{
    int validez;
    char codigo[8];
    char descripcion[15];
    int cantidad;
    float costo;
} productos;

void ingreso(FILE* stock)
{
    int opcion;
    char confirmar;
    productos nuevo;
    fseek(stock,0,SEEK_END);
    printf("\t\t\tINGRESO DE MERCADERIA\n\n");
    printf("CODIGO: ");
    fflush(stdin);
    gets(nuevo.codigo);
    printf("\nDESCRIPCION: ");
    fflush(stdin);
    gets(nuevo.descripcion);
    printf("\nCANTIDAD: ");
    fflush(stdin);
    scanf("%d",&nuevo.cantidad);
    printf("\nCOSTO: ");
    fflush(stdin);
    scanf("%f",&nuevo.costo);
    printf("Desea confirmar producto?(s/n) ");
    fflush(stdin);
    scanf("%c",&confirmar);
    if(confirmar=='s')
    {
        nuevo.validez=1;
        fwrite(&nuevo,sizeof(productos),1,stock);
        fflush(stock);
    }
    system("pause");
    system("cls");
}

void gotoxy(int x, int y)
{
COORD coord;
coord.X=x;
coord.Y=y;
SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),coord);
}

void listado(FILE* stock)
{
    productos lista;
    fseek(stock,0,SEEK_SET);
    int aux=0, y=2;
    printf("Codigo");
    gotoxy(10,0);
    printf("|Descripcion");
    gotoxy(27,0);
    printf("|Cantidad");
    gotoxy(37,0);
    printf("|Costo");
    gotoxy(44,0);
    printf("|Importe\n");
    fread(&lista,sizeof(productos),1,stock);
    while (feof(stock)==0)
    {
        if(lista.validez==1)
        {
            gotoxy(0,y);
            printf("|%s",lista.codigo);
            gotoxy(10,y);
            printf("|%s",lista.descripcion);
            gotoxy(27,y);
            printf("|%d",lista.cantidad);
            gotoxy(37,y);
            printf("|%5.2f",lista.costo);
            gotoxy(44,y);
            printf("|%5.2f",(lista.cantidad*lista.costo));
            printf("\n");
            fread(&lista,sizeof(productos),1,stock);
            y++;
        }
    }

    system("pause");
    system("cls");
}

int menu(FILE* stock)
{
    int opcion;
    printf("\t\t\t\t\tMENU\n");
    printf("\n\n1. Ingresar mercaderia.");
    printf("\n2. Emitir listado valorizado del stock actual.");
    printf("\n0. Salir del programa.\n\n");
    printf("Opcion: ");
    fflush(stdin);
    scanf("%d",&opcion);
    switch(opcion)
    {
    case 1:
        {
            system("cls");
            ingreso(stock);
            break;
        }
    case 2:
        {
            system("cls");
            listado(stock);
            break;
        }
    case 0:
        {
            return 999;
            break;
        }
    }
}

main()
{
    FILE* stock;
    int aux,largo;
    stock=fopen("Stock.sss","rb+");
    if(stock==NULL)
    {
        stock=fopen("Stock.sss","wb+");
    }
    do
    {
        aux=menu(stock);
    } while(aux!=999);
    fclose(stock);
}
