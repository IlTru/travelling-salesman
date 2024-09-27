#include <iostream>
#include <algorithm>
#include <vector>
#include <fstream>

using namespace std;

const int kNrOrase = 10, kNrCromozomiPerPopulatie = 10, kNrParintiGenerati = 4, kIteratiiTotale = 1;
const char* kOrase[kNrOrase] = { "Craiova", "Bucuresti", "Iasi", "Cluj-Napoca", "Timisoara", "Constanta", "Brasov", "Galati", "Oradea", "Sibiu" };
int distante[kNrOrase][kNrOrase];

int CalculeazaFitness(vector<int> cromozom){
    int fitness = 0;
    for (int i = 0; i<kNrOrase-1; i++)
        fitness = fitness + distante[cromozom[i]][cromozom[i+1]];

    return fitness;
}

double CalculeazaFactorial(int n){
    double fact = 1;
    for (int i = 2; i <= n; ++i) {
        fact *= i;
    }

    return fact;
}

void AfiseazaPopulatie(vector<vector<int>> populatie){
    for (int i = 0; i < populatie.size(); i++) {
        for (int j = 0; j < kNrOrase; j++) {
            cout << populatie[i][j] << " ";
        }
        cout << "fitness = " << CalculeazaFitness(populatie[i]);
        cout << endl;
    }
    cout << endl;
}

void AfiseazaTraseu(vector<int> cromozom){
    cout << kOrase[cromozom[0]];
    for (int i = 1; i < kNrOrase; i++) {
        cout << " -> " << kOrase[cromozom[i]]; /* pentru fiecare geana a cromozomului afisez orasul corespunzator */
    }
    cout << endl;
}

vector<vector<int>> InitializeazaPopulatie(){
    vector<vector<int>> populatie(kNrCromozomiPerPopulatie, vector<int>(kNrOrase));
    for (int i = 0; i < kNrCromozomiPerPopulatie; i++) {
        int cromozom[kNrOrase];
        for (int j = 0; j < kNrOrase; j++)
            cromozom[j] = j;
        random_shuffle(begin(cromozom),end(cromozom)); /*formez un cromozom simplu cu elemente de la 0 la kNrOrase si schimb ordinea genelor aleator */
        for (int j = 0; j < kNrOrase; j++) {
            populatie[i][j] = cromozom[j];
        }
    }

    return populatie;
}

vector<vector<int>> SelectiaTurneu(vector<vector<int>> populatie, int nrTurnee, int nrCromPerTurneu){
    vector<vector<int>> parintiSelectati(nrTurnee, vector<int>(kNrOrase));
    for (int i = 0; i < nrTurnee; i++) {
        int cromozomiAleatori[nrCromPerTurneu];
        for(int j = 0; j < nrCromPerTurneu; j++)
            cromozomiAleatori[j] = rand() % kNrCromozomiPerPopulatie; /* generez un vector cu pozitii random ce reprezinta pozitiile cromozomilor din populatie */

        int indexCromozomAles = cromozomiAleatori[0]; /* aplic metoda turneu cromozomilor alesi random si il selectez pe cel cu fitness-ul cel mai mic */
        for (int j = 1; j < nrCromPerTurneu; j++) {
            if (CalculeazaFitness(populatie[indexCromozomAles]) > CalculeazaFitness(populatie[cromozomiAleatori[j]]))
                indexCromozomAles = cromozomiAleatori[j];
        }

        parintiSelectati[i] = populatie[indexCromozomAles];
    }

    return parintiSelectati;
}

bool VerificaElement(vector<int> copil, int elem) {
    for (int i = 0; i < kNrOrase; i++)
        if (copil[i] == elem)
            return true;
    return false;
}

vector<vector<int>> incrucisareaDeOrdineOX(vector<vector<int>>& parintiSelectati){
    int nrCopiiDeGenerat = (CalculeazaFactorial(kNrParintiGenerati) / (2 * CalculeazaFactorial(kNrParintiGenerati - 2))) * 2; /* calculez numarul copiilor de generat considerand faptul ca fiecare parinte se va incrucisa o singura data cu toti ceilalti si nu se va incucisa cu el insusi*/
    vector<vector<int>> copiiGenerati(nrCopiiDeGenerat, vector<int>(kNrOrase));

    int indexCopiiGenerati = 0;
    for (int i = 0; i < kNrParintiGenerati-1; i++) {
        for (int j = i+1; j < kNrParintiGenerati; j++) {
            vector<int> parinte1(kNrOrase), parinte2(kNrOrase), copil1(kNrOrase), copil2(kNrOrase);
            parinte1 = parintiSelectati[i];
            parinte2 = parintiSelectati[j];
            int punctDeTaiere1 = rand() % (kNrOrase - 2); /* se aleg in mod aleator doua puncte de taiere */
            int punctDeTaiere2 = rand() % (kNrOrase - 1);
            while (punctDeTaiere2 <= punctDeTaiere1) /* punctDeTaiere2 trebuie sa fie mai mare si diferit de punctDeTaiere1 */
                punctDeTaiere2 = rand() % (kNrOrase - 1);
            for (int k = 0; k < kNrOrase; ++k) { /* se initializeaza copii cu valori de '-1' (valori de completat) */
                copil1[k] = -1;
                copil2[k] = -1;
            }
            for (int k = punctDeTaiere1; k <= punctDeTaiere2; k++) { /* intre punctele de taiere se copiaza valorile */
                copil1[k] = parinte1[k];
                copil2[k] = parinte2[k];
            }

            vector<int> aux1(kNrOrase), aux2(kNrOrase);
            int index = 0;
            for (int k = punctDeTaiere2 + 1; k < kNrOrase; k++) { /* se initializeaza si construiesc cromozomii auxiliari */
                aux1[index] = parinte1[k];
                aux2[index] = parinte2[k];
                index++;
            }

            for (int k = 0; k <= punctDeTaiere2; k++) {
                aux1[index] = parinte1[k];
                aux2[index] = parinte2[k];
                index++;
            }

            int indexAux = 0; /* completez vectorul copil1 cu elemente din vectorul aux2 ce nu se regasesc in vectorul copil1 */
            int indexCopil = punctDeTaiere2+1;
            while (indexCopil < kNrOrase){
                if (VerificaElement(copil1, aux2[indexAux]))
                    indexAux++;
                else {
                    copil1[indexCopil] = aux2[indexAux];
                    indexCopil++;
                    indexAux++;
                }
            }
            indexCopil = 0;
            while (indexCopil < punctDeTaiere1){
                if (VerificaElement(copil1, aux2[indexAux]))
                    indexAux++;
                else {
                    copil1[indexCopil] = aux2[indexAux];
                    indexCopil++;
                    indexAux++;
                }
            }

            indexAux = 0;
            indexCopil = punctDeTaiere2+1;
            while (indexCopil < kNrOrase){ /* completez vectorul copil2 cu elemente din vectorul aux1 ce nu se regasesc in vectorul copil2 */
                if (VerificaElement(copil2, aux1[indexAux]))
                    indexAux++;
                else {
                    copil2[indexCopil] = aux1[indexAux];
                    indexCopil++;
                    indexAux++;
                }
            }
            indexCopil = 0;
            while (indexCopil < punctDeTaiere1){
                if (VerificaElement(copil2, aux1[indexAux]))
                    indexAux++;
                else {
                    copil2[indexCopil] = aux1[indexAux];
                    indexCopil++;
                    indexAux++;
                }
            }

            copiiGenerati[indexCopiiGenerati] = copil1;
            indexCopiiGenerati++;
            copiiGenerati[indexCopiiGenerati] = copil2;
            indexCopiiGenerati++;
        }
    }
    return copiiGenerati;
}

vector<vector<int>> mutatiaSpecificaPrinSchimbare(vector<vector<int>> copii){
    float probabilitateDeMutatie = 0.2; /* decid de la inceput probabilitatea de mutatie */

    for (int i = 0; i < copii.size(); ++i) {
        float p = (rand() % 100)/100.f; /* generez o valoare p pentru fiecare cromozom si atunci cand aceasta este mai mica decat probabilitateaDeMutatie aplic mutatia pe acel cromozom */
        if (p < probabilitateDeMutatie){
            int indexGeana1 = rand() % kNrOrase; /* se aleg in mod aleator doua puncte de taiere */
            int indexGeana2 = rand() % kNrOrase;
            while (indexGeana2 <= indexGeana1) /* punctDeTaiere2 trebuie sa fie mai mare si diferit de punctDeTaiere1 */
                indexGeana2 = rand() % kNrOrase;
            int aux = copii[i][indexGeana1];
            copii[i][indexGeana1] = copii[i][indexGeana2];
            copii[i][indexGeana2] = aux;
        }
    }
    return copii;
}

int main() {
    srand(time(0));
    ifstream f("matricea_distantelor.txt");
    for (int i = 0; i < kNrOrase; i++)
        for (int j = 0; j < kNrOrase; j++) {
            f >> distante[i][j];
        }

    vector<vector<int>> populatieGenerata = InitializeazaPopulatie();
    cout << "Populatia initiala: " << endl;
    AfiseazaPopulatie(populatieGenerata);

    for (int i = 0; i < kIteratiiTotale; i++) {
        vector<vector<int>> parintiSelectati = SelectiaTurneu(populatieGenerata, kNrParintiGenerati, 5);
        cout << "Parintii selectati in urma selectiei turneu: " << endl;
        AfiseazaPopulatie(parintiSelectati);

        vector<vector<int>> copiiGenerati = incrucisareaDeOrdineOX(parintiSelectati);
        cout << "Copii generati in urma incrucisarii de ordine OX: " << endl;
        AfiseazaPopulatie(copiiGenerati);

        vector<vector<int>> copiiDupaMutatii = mutatiaSpecificaPrinSchimbare(copiiGenerati);
        cout << "Copii in urma mutatiei specifica prin schimbare: " << endl;
        AfiseazaPopulatie(copiiDupaMutatii);

        populatieGenerata.insert(populatieGenerata.end(), copiiDupaMutatii.begin(),copiiDupaMutatii.end()); /* concatenam copii generati populatiei initiale si mai apoi facem o reselectie a populatiei */
        cout << "Concatenarea dintre populatia initiala si copii generati: " << endl;
        AfiseazaPopulatie(populatieGenerata);

        populatieGenerata = SelectiaTurneu(populatieGenerata, kNrCromozomiPerPopulatie, 5);
        cout << "Populatia finala: " << endl;
        AfiseazaPopulatie(populatieGenerata);
    }

    int indexCelMaiBunTraseu = 0;
    for (int i = 1; i < populatieGenerata.size(); i++) {
        if (CalculeazaFitness(populatieGenerata[indexCelMaiBunTraseu]) > CalculeazaFitness(populatieGenerata[i]))
            indexCelMaiBunTraseu = i;
    }

    cout << "Cel mai bun traseu gasit este urmatorul: " << endl;
    AfiseazaTraseu(populatieGenerata[indexCelMaiBunTraseu]);
    cout << endl << "Distanta totala: " << CalculeazaFitness(populatieGenerata[indexCelMaiBunTraseu]) << "km";

    return 0;
}
