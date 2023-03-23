import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Activity } from '../dto/activity';
import { Progress } from '../dto/progress';
import { Street } from '../dto/street';

@Injectable({
  providedIn: 'root'
})
export class ActivitiesService {
  private apiServerUrl = environment.apiUri;

  constructor(private http: HttpClient) { 
  }

  public getActivities(page: number = 0): Observable<Activity[]> {
    let params = new HttpParams().set('page', page);
    return this.http.get<Activity[]>(`${this.apiServerUrl}/activities`, { params: params });
  }

  public getStreets(page: number = 0): Observable<Street[]> {
    let params = new HttpParams().set('page', page);
    return this.http.get<Street[]>(`${this.apiServerUrl}/streets`, { params: params });
  }

  public getProgress(): Observable<Progress> {
    return this.http.get<Progress>(`${this.apiServerUrl}/streets/progress`);
  }
}
