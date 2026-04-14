using System.Globalization;

namespace BiometricoDemo;

public sealed record Minutia(int X, int Y, double Angle);

public sealed class FingerprintTemplate
{
    public FingerprintTemplate(string personId, string fullName, IReadOnlyList<Minutia> minutiae)
    {
        PersonId = personId;
        FullName = fullName;
        Minutiae = minutiae;
    }

    public string PersonId { get; }
    public string FullName { get; }
    public IReadOnlyList<Minutia> Minutiae { get; }
}

public sealed class BiometricMatcher
{
    private const int MaxDistance = 9;
    private const double MaxAngleDifference = 12.0;

    public double Compare(FingerprintTemplate registered, FingerprintTemplate sample)
    {
        var matches = 0;

        foreach (var source in sample.Minutiae)
        {
            var found = registered.Minutiae.Any(target =>
                Distance(source, target) <= MaxDistance &&
                AngleDifference(source.Angle, target.Angle) <= MaxAngleDifference);

            if (found)
            {
                matches++;
            }
        }

        return (double)matches / Math.Max(sample.Minutiae.Count, registered.Minutiae.Count);
    }

    private static double Distance(Minutia first, Minutia second)
    {
        var dx = first.X - second.X;
        var dy = first.Y - second.Y;
        return Math.Sqrt(dx * dx + dy * dy);
    }

    private static double AngleDifference(double first, double second)
    {
        var difference = Math.Abs(first - second) % 360;
        return difference > 180 ? 360 - difference : difference;
    }
}

internal static class Program
{
    private static readonly List<FingerprintTemplate> Database =
    [
        new("1001", "Ana Morales", [
            new(14, 30, 15), new(28, 44, 35), new(42, 61, 58), new(58, 73, 72), new(70, 81, 91)
        ]),
        new("1002", "Carlos Rojas", [
            new(11, 20, 8), new(24, 36, 25), new(39, 47, 41), new(55, 65, 64), new(69, 78, 83)
        ]),
        new("1003", "Diana Ruiz", [
            new(16, 28, 18), new(31, 45, 38), new(43, 62, 61), new(59, 74, 75), new(72, 80, 92)
        ])
    ];

    public static void Main()
    {
        var matcher = new BiometricMatcher();
        var sample = new FingerprintTemplate("sample", "Huella capturada", [
            new(15, 31, 17), new(30, 46, 36), new(44, 63, 60), new(60, 73, 76), new(73, 82, 93)
        ]);

        Console.WriteLine("Prototipo academico de autenticacion biometrica");
        Console.WriteLine("Comparando huella capturada contra registros locales...\n");

        var results = Database
            .Select(person => new { Person = person, Score = matcher.Compare(person, sample) })
            .OrderByDescending(result => result.Score)
            .ToList();

        foreach (var result in results)
        {
            Console.WriteLine($"{result.Person.PersonId} - {result.Person.FullName}: {result.Score.ToString("P1", CultureInfo.InvariantCulture)}");
        }

        var best = results.First();
        Console.WriteLine();
        Console.WriteLine(best.Score >= 0.80
            ? $"Acceso aprobado para {best.Person.FullName}."
            : "Acceso rechazado. No hay coincidencia suficiente.");
    }
}
