package Controladores;

import Model.Metadatos;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class Controllers {

    private static List<Metadatos> metadatos = new ArrayList<>();

    public static void construirMetadatos(String folderPath) {
        try {
            Path path = Paths.get(folderPath);
            Files.walk(path)
                    .filter(Files::isRegularFile)
                    .forEach(file -> {
                        try {
                            String content = new String(Files.readAllBytes(file));
                            String nombre = file.getFileName().toString();
                            Metadatos metadato = new Metadatos(nombre, content);
                            metadatos.add(metadato);
                        } catch (IOException e) {
                            System.err.println("Error al leer el archivo: " + file.getFileName());
                            e.printStackTrace();
                        }
                    });
        } catch (IOException e) {
            System.err.println("Error al acceder a la carpeta: " + folderPath);
            e.printStackTrace();
        }
    }

    public static int combinarYGuardarArticulos(String outputFilePath) {
        List<String> contenidoUnico = new ArrayList<>();


        for (int i = 0; i < metadatos.size(); i++) {
            String contenido = metadatos.get(i).getContenido();
            String[] articulos = contenido.split("TY  - ");

            for (int j = 1; j < articulos.length; j++) {
                String articulo = "TY  - " + articulos[j];

                if (!articuloYaIncluido(contenidoUnico, articulo)) {
                    contenidoUnico.add(articulo);
                }
            }
        }


        try (FileWriter writer = new FileWriter(outputFilePath)) {
            for (int k = 0; k < contenidoUnico.size(); k++) {
                writer.write(contenidoUnico.get(k));
                writer.write(System.lineSeparator());
            }
            System.out.println("Archivo creado con éxito en: " + outputFilePath);
        } catch (IOException e) {
            System.err.println("Error al escribir en el archivo: " + outputFilePath);
            e.printStackTrace();
        }


        return contenidoUnico.size();
    }

    private static boolean articuloYaIncluido(List<String> contenidoUnico, String articulo) {
        for (String contenido : contenidoUnico) {
            if (contenido.equals(articulo)) {
                return true;
            }
        }
        return false;
    }

    public static Metadatos encontrarArticuloMasCompleto() {
        if (metadatos.isEmpty()) {
            return null;
        }

        Metadatos articuloMasCompleto = metadatos.get(0);

        for (int i = 1; i < metadatos.size(); i++) {
            if (metadatos.get(i).getContenido().length() > articuloMasCompleto.getContenido().length()) {
                articuloMasCompleto = metadatos.get(i);
            }
        }

        return articuloMasCompleto;
    }

    public static void main(String[] args) {
        construirMetadatos("Articulos");
        int totalArticulosUnicos = combinarYGuardarArticulos("articulos_combinados.txt");
        System.out.println("Total de artículos únicos en el archivo combinado: " + totalArticulosUnicos);

    }
}
