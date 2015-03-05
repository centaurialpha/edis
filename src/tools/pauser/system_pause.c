/* 
 * EDIS - a simple cross-platform IDE for C
 * 
 * Ejecuta un proceso y pausa
 *
 * This file is part of Edis
 * Copyright 2014-2015 - Edis Team
 * License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

/* Prototipos */
void pauser( int exit, double time_used );
void executeCommand( char * command );

int main( int argc, char** argv ) {
    if( argc > 1 ){
    	/* Tiempo inicial y tiempo final */
    	time_t start, end;
    	/* Tiempo usado por el proceso */
    	double time_used;
    	/* Título en consola */
    	SetConsoleTitle( argv[1] );
    	/* Programa a ejecutar */
    	char * command = argv[1];
    	/* Inicio segundos */
    	start = clock();
    	/* Ejecución del comando */
    	executeCommand( command );
    	/* Fin de ejecución */
    	end = clock();
    	time_used = (( double) ( end - start)) / CLOCKS_PER_SEC;
    	/* Pausa */
    	pauser( EXIT_SUCCESS, time_used );
    	
	}
        
    return 0;
}

void pauser( int exit_code, double time_used ) {
	printf( "\n\n---------------------------------" );
	printf( "\nEl programa ha terminado despu%cs de %.3g segundos\n", 130, time_used );
	system( "pause" );
	exit( exit_code );
}

void executeCommand( char * command ) {
	/* Run ! */
    system( command );
}
