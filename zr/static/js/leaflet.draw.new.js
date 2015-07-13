/**
 * Created by marcinra on 1/19/14.
 */
L.drawVersion = '0.2.4-dev';

L.drawLocal = {
        draw: {
                toolbar: {
                        actions: {
                                title: 'Anuluj rysowanie',
                                text: 'Anuluj'
                        },
                        undo: {
                                title: 'Usuń ostatni punkt rysowania',
                                text: 'Usuń ostatni punkt'
                        },
                        buttons: {
                                polyline: 'Narysuj linię na mapie i dodaj nowy komentarz ',
                                polygon: 'Narysuj obszar na mapie i dodaj nowy komentarz',
                                rectangle: 'Wyszukaj z mapy',
                                circle: 'Narysuj okrąg',
                                marker: 'Umieść punkt na mapie i dodaj nowy komentarz'
                        }
                },
                handlers: {
                        circle: {
                                tooltip: {
                                        start: 'Kliknij i przeciągnij, aby narysować okrąg.'
                                }
                        },
                        marker: {
                                tooltip: {
                                        start: 'Kliknij na mapę, aby umieścić znacznik.'
                                }
                        },
                        polygon: {
                                tooltip: {
                                        start: 'Kliknij, aby rozpocząć rysowanie.',
                                        cont: 'Kliknij aby kontynuować rysowanie kształtu.',
                                        end: 'Kliknij pierwszy punkt, aby zamknąć obszar.'
                                }
                        },
                        polyline: {
                                error: '<strong> Błąd: </ strong> krawędzi kształtów nie może przekroczyć!',
                                tooltip: {
                                        start: 'Kliknij, aby rozpocząć rysowanie.',
                                        cont: 'Kliknij aby kontynuować rysowanie lini.',
                                        end: 'Kliknij ostatni punkt, aby zamknąć obszar.'
                                }
                        },
                        rectangle: {
                                tooltip: {
                                        start: 'Kliknij i przeciągnij, aby narysować prostokąt.'
                                }
                        },
                        simpleshape: {
                                tooltip: {
                                        end: 'Zwolnij myszy, aby zakończyć rysowanie.'
                                }
                        }
                }
        },
        edit: {
                toolbar: {
                        actions: {
                                save: {
                                        title: 'Save changes.',
                                        text: 'Save'
                                },
                                cancel: {
                                        title: 'Cancel editing, discards all changes.',
                                        text: 'Cancel'
                                }
                        },
                        buttons: {
                                edit: 'Edit layers.',
                                editDisabled: 'No layers to edit.',
                                remove: 'Delete layers.',
                                removeDisabled: 'No layers to delete.'
                        }
                },
                handlers: {
                        edit: {
                                tooltip: {
                                        text: 'Drag handles, or marker to edit feature.',
                                        subtext: 'Click cancel to undo changes.'
                                }
                        },
                        remove: {
                                tooltip: {
                                        text: 'Click on a feature to remove'
                                }
                        }
                }
        }
};
